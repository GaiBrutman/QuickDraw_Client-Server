from __future__ import print_function, division

import argparse

import random

import socket
from threading import Thread

import numpy as np

import torch
import torch.nn.functional as F

from PIL import Image

from dataset import get_transforms
from model import QuickDrawNet

Classes = None


class Server(object):
    MAX_CLIENTS = 20

    def __init__(self, model_path):
        super(Server, self).__init__()
        self.my_socket = None

        self.n_clients = 0

        self.guesses = []
        print(model_path)
        self.model = QuickDrawNet.load_from_file(model_path)
        self.model.eval()

        _, self.transform = get_transforms()

    def start_connections(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.bind(('', 1235))

        self.my_socket.listen(self.MAX_CLIENTS)
        print('\nServer is listening...')

        while self.n_clients < self.MAX_CLIENTS:
            (other_socket, other_address) = self.my_socket.accept()
            client_t = Thread(target=self.handle_client, args=(other_socket,))
            client_t.start()
            print('Client %d is connected.' % self.n_clients)
            self.n_clients += 1

    def end_connection(self, other_sock=None, close_server=False):
        print('Closed connection with %s.' % other_sock)

        if close_server and self.my_socket:
            self.my_socket.close()
        if other_sock:
            other_sock.close()

    @staticmethod
    def receive_chunks(sock, verbose=False):
        data = ''
        recv = str(sock.recv(1024), encoding='utf-8')
        while recv[-3:] != '!@#':
            data += recv
            recv = str(sock.recv(1024), encoding='utf-8')

        data += recv
        data = data.split('!@#')
        data = data[0] if len(data) > 1 else ' '.join(['0'] * 784)

        if verbose:
            print('Received:', data[:6], '...', data[-6:])
        return data

    def guess_percentages(self, sock, msg=None, verbose=False):
        array_str = self.receive_chunks(sock) if msg is None else msg

        if not array_str:
            return None

        try:
            img = np.array([int(x) for x in array_str.split(' ')]).reshape(28, 28)
        except ValueError as e:
            print(len(array_str.split(' ')), array_str.split(' '))
            raise e
        img = Image.fromarray(img.astype(np.uint8))
        img = self.transform(img)

        with torch.no_grad():
            out = self.model(img[None])
            pred = F.softmax(out, dim=1)

            pred = np.squeeze(np.asfarray(pred))

        sorted_pred_indices = np.argsort(-pred)[:3]

        if verbose:
            for a in sorted_pred_indices:
                print('%s - %0.3f' % (CLASSES[a], pred[a]))

        return ','.join(["%s:%.3f" % (CLASSES[i], pred[i] * 100) for i in sorted_pred_indices])

    def receive_and_send(self, client_sock, msg=None, verbose=False):
        current_guess = self.guess_percentages(client_sock, msg)
        if not current_guess:
            return False

        if verbose:
            print('sending', current_guess)

        # send prediction and get whether it is right
        client_sock.send((current_guess + '\n').encode())

        return True

    def handle_client(self, client_sock):
        example = ' / '.join([CLASSES[i] for i in random.sample(set(range(10)), 3)])  # get three unique categories
        client_sock.send((example + '\n').encode())

        ret = True
        while ret:
            try:
                ret = self.receive_and_send(client_sock)
            except socket.error:
                break
        self.end_connection(client_sock)
        self.n_clients -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_connection(close_server=True)


def parse():
    parser = argparse.ArgumentParser(description='QuickDraw drawing classifier server')
    parser.add_argument('-cp', '--categories_path', help='Path of categories file')
    parser.add_argument('-sm', '--saved_model', help='path of saved model to use (with .pth extension)')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    server_args = parse()

    print('QuickDraw Server (Ctrl-C to Exit)\n')

    assert server_args.categories_path and server_args.saved_model

    with open(server_args.categories_path, 'r') as f:
        CLASSES = [s.upper() for s in f.read().splitlines()]

    with Server(server_args.saved_model) as s:
        connect_t = Thread(target=s.start_connections)
        connect_t.setDaemon(True)
        connect_t.start()

        while True:
            try:
                pass
            except KeyboardInterrupt:
                break
