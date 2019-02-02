from __future__ import print_function, division

import numpy as np
import pandas as pd

import torch
from torchvision import transforms
from torch.utils.data import Dataset

import PIL
from PIL import Image


class QuickDrawDataset(Dataset):
    """QuickDraw drawings dataset."""

    def __init__(self, csv_file, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with drawings and labels.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """

        df = pd.read_csv(csv_file)
        columns = df.columns

        self.labels = torch.from_numpy(df[columns[0]].values).long()

        self.drawings = df[columns[1:]].values

        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        drawing = self.drawings[idx].reshape(28, 28)

        image = Image.fromarray(drawing.astype(np.uint8))

        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label


def get_transforms():
    train_composed = transforms.Compose([
        transforms.ColorJitter(hue=.05, saturation=.05),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(20, resample=PIL.Image.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    test_composed = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    return train_composed, test_composed
