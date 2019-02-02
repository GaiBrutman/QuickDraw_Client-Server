#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function, division

import argparse

import torch
from torch.utils.data import DataLoader

from dataset import QuickDrawDataset, get_transforms
from model import QuickDrawNet

USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda:0" if USE_CUDA else "cpu")

CLASSES = []


def load_prepare_data(test_path, verbose=True):
    assert CLASSES

    _, test_transform = get_transforms()

    test_ds = QuickDrawDataset(csv_file=test_path, transform=test_transform)
    test_dl = DataLoader(test_ds, batch_size=64, shuffle=False, num_workers=0)

    if verbose:
        print('Number of classes:', len(CLASSES))
        print('Test: %d' % len(test_ds))

    return test_ds, test_dl


def evaluate_total(model, test_dl):
    model.eval()

    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_dl:
            inputs, labels = [x.to(device) for x in data]

            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print('Accuracy of the network on the 10000 test images: %.1f %%\n' % (100. * correct / total))


def evaluate_classes(model, test_dl):
    class_correct = list(0. for i in range(55))
    class_total = list(0. for i in range(55))
    with torch.no_grad():
        for data in test_dl:
            inputs, labels = [x.to(device) for x in data]

            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            c = (predicted == labels).squeeze()
            for i in range(4):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1

    for i in range(len(CLASSES)):
        print('Accuracy of %5s : %.1f %%\n' % (CLASSES[i], 100. * class_correct[i] / class_total[i]))


def evaluate(model, test_path, eval_classes):
    print()

    test_ds, test_dl = load_prepare_data(test_path, verbose=True)
    print('Data loaded\n')

    print('device: %s\n' % device)
    model.to(device)

    print('Evaluation started\n')

    evaluate_total(model, test_dl)

    if eval_classes:
        evaluate_classes(model, test_dl)

    print('Done Evaluating')


def parse():
    parser = argparse.ArgumentParser(description='QuickDraw drawing classifier evaluation')
    parser.add_argument('-cp', '--categories_path', help='Path of categories file')
    parser.add_argument('-ts', '--test_path', help='Path of test data')
    parser.add_argument('-sm', '--saved_model', help='path of saved model to evaluate (with .pth extension)')
    parser.add_argument('-ec', '--eval_classes', action='store_true',
                        help='Evaluate Performance of model on every class')

    args = parser.parse_args()
    return args


def run(args):
    global CLASSES

    print('args: %s' % vars(args))

    print('\nStart\n')

    assert args.categories_path and args.test_path and args.saved_model

    with open(args.categories_path, 'r') as f:
        CLASSES = [s.upper() for s in f.read().splitlines()]

    assert CLASSES

    model = QuickDrawNet.load_from_file(args.saved_model, verbose=True)

    evaluate(model, args.test_path, args.eval_classes)

    print('\nDone\n')


def main():
    eval_args = parse()
    run(eval_args)


if __name__ == '__main__':
    main()
