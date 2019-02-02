import torch
import torch.nn as nn
import torch.nn.functional as F


class QuickDrawNet(nn.Module):
    def __init__(self, n_classes, n_c1=32, n_fc=512, dropout=0.):
        super(QuickDrawNet, self).__init__()
        self.n_c1 = n_c1
        self.n_fc = n_fc
        self.n_classes = n_classes

        self.conv1 = nn.Conv2d(1, n_c1, 3)
        self.conv2 = nn.Conv2d(n_c1, n_c1, 3)
        self.conv3 = nn.Conv2d(n_c1, n_c1 * 2, 3)
        self.conv4 = nn.Conv2d(n_c1 * 2, n_c1 * 2, 3)

        self.bn1 = nn.BatchNorm2d(n_c1)
        self.bn2 = nn.BatchNorm2d(n_c1 * 2)
        self.bn3 = nn.BatchNorm1d(n_fc)

        self.pool = nn.MaxPool2d(2, 2)

        self.dropout = nn.Dropout(p=dropout)

        self.fc1 = nn.Linear(n_c1 * 2 * 4 * 4, n_fc)
        self.fc2 = nn.Linear(n_fc, n_classes)

    @staticmethod
    def load_from_file(fn, verbose=True):
        params = torch.load(fn, map_location='cpu')

        n_classes = params['fc2.weight'].size(0)
        n_c1 = params['conv1.weight'].size(0)
        n_fc = params['bn3.weight'].size(0)

        if verbose:
            print('Loaded model:\n\tn_classes: %d\n\tn_c1: %d\n\tn_fc: %d' % (n_classes, n_c1, n_fc))

        model = QuickDrawNet(n_classes, n_c1=n_c1, n_fc=n_fc)
        model.load_state_dict(params)
        return model

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(F.relu(self.conv2(x)))

        x = F.relu(self.conv3(x))
        x = self.pool(F.relu(self.conv4(x)))

        x = x.view(-1, self.n_c1 * 2 * 4 * 4)
        x = self.dropout(F.relu(self.fc1(x)))

        x = self.fc2(x)
        return x
