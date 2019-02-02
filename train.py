#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import time

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader

import argparse
from tqdm import tqdm

from dataset import QuickDrawDataset, get_transforms
from model import QuickDrawNet

CLASSES = []

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda:0" if USE_CUDA else "cpu")


def load_prepare_data(train_path, val_path, batch_size, shuffle, verbose=True):
    assert CLASSES

    train_transform, val_transform = get_transforms()

    train_ds = QuickDrawDataset(csv_file=train_path, transform=train_transform)
    train_dl = DataLoader(train_ds, batch_size=batch_size,
                          shuffle=shuffle, num_workers=0)

    val_ds, val_dl = None, None
    if val_path:
        val_ds = QuickDrawDataset(csv_file=val_path, transform=val_transform)
        val_dl = DataLoader(val_ds, batch_size=batch_size,
                            shuffle=shuffle, num_workers=0)

    if verbose:
        print('Number of classes:', len(CLASSES))
        print('Train: %d, Valid: %d' % (len(train_ds), len(val_ds) if val_ds else 0))

    return train_ds, train_dl, val_ds, val_dl


def one_step(model, data, optimizer, criterion, mode='train'):
    # get the inputs
    inputs, labels = [x.to(device) for x in data]

    # zero the parameters gradients
    optimizer.zero_grad()

    # forward
    outputs = model(inputs)
    loss = criterion(outputs, labels)

    if mode == 'train':
        # backward + optimize
        loss.backward()
        optimizer.step()

    return loss.item()


def train(model, train_path, val_path, shuffle, epochs, batch_size, learning_rate):
    print()

    train_ds, train_dl, val_ds, val_dl = load_prepare_data(train_path, val_path, batch_size, shuffle)
    print('Data loaded\n')

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    print('device: %s\n' % device)
    model.to(device)

    print('Training started\n')
    time.sleep(0.01)

    for e in range(epochs):
        t_train = tqdm(train_dl, desc='Epoch %d' % e)

        running_loss = 0.

        model.train()
        for i, data in enumerate(t_train, 0):

            train_loss = one_step(model, data, optimizer, criterion, mode='train')

            running_loss += train_loss
            if i + 1 == len(t_train):
                if val_dl:
                    running_val_loss = 0.
                    model.eval()
                    with torch.no_grad():
                        for j, val_data in enumerate(val_dl, 0):
                            val_loss = one_step(model, val_data, optimizer, criterion, mode='valid')
                            running_val_loss += val_loss

                    t_train.set_postfix(loss=running_loss / len(t_train), val_loss=running_val_loss / len(val_dl))
                else:
                    t_train.set_postfix(loss=running_loss / len(t_train))
            else:
                t_train.set_postfix(loss=running_loss / (i + 1))

    print('\nDone Training')


def parse():
    parser = argparse.ArgumentParser(description='QuickDraw drawing classifier train')
    parser.add_argument('-cp', '--categories_path', help='Path of categories file')
    parser.add_argument('-tr', '--train_path', help='Path of train data')
    parser.add_argument('-vl', '--val_path', help='Path of validation data (optional)')
    parser.add_argument('-ts', '--to_save', help='Path to save trained model in (with .pth extension)')
    parser.add_argument('-sm', '--saved_model', help='saved model for additional training')
    parser.add_argument('-sh', '--shuffle', action='store_true', help='Shuffle the data')
    parser.add_argument('-nc', '--n_channels', type=int, default=32,
                        help='#channels for the first conv layer (multiplied by 2 in the second)')
    parser.add_argument('-hi', '--hidden', type=int, default=512, help='hidden size for fully connected layer')
    parser.add_argument('-e', '--epochs', type=int, default=5, help='Train the model with e epochs')
    parser.add_argument('-b', '--batch_size', type=int, default=64, help='Batch size')
    parser.add_argument('-lr', '--learning_rate', type=float, default=0.002, help='Learning rate')
    parser.add_argument('-d', '--dropout', type=float, default=0.2, help='Dropout probability')

    args = parser.parse_args()
    return args


def run(args):
    global CLASSES

    print('args: %s' % vars(args))

    print('\nStart\n')

    if not args.to_save:
        args.to_save = 'models\\saved_model.pth'

    assert args.categories_path and args.train_path

    with open(args.categories_path, 'r') as f:
        CLASSES = [s.upper() for s in f.read().splitlines()]

    assert CLASSES

    model = QuickDrawNet(n_classes=len(CLASSES), n_c1=args.n_channels, n_fc=args.hidden, dropout=args.dropout)
    if args.saved_model:
        model.load_state_dict(torch.load(args.saved_model))

    train(model, args.train_path, args.val_path, args.shuffle, args.epochs, args.batch_size, args.learning_rate)

    torch.save(model.state_dict(), args.to_save)
    print('Saved model in %s' % args.to_save)

    print('\nDone')


def main():
    train_args = parse()
    run(train_args)


if __name__ == '__main__':
    main()
