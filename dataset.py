from re import A
from matplotlib import transforms
from spacy import load
import torch
from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
import os
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
class featureDataset(Dataset):
    def __init__(self, ):
        self.sscaler = StandardScaler()
        self.mmscaler = MinMaxScaler()

    def __getitem__(self, index):
        with open(f'features/{index}.npy', 'rb') as f:
            data = np.load(f)
            data = np.expand_dims(data, axis=1)
            data = self.sscaler.fit_transform(data)
            data = self.mmscaler.fit_transform(data)
            data = torch.tensor(data).reshape(1, 48)
        with open(f'gtnp/{index}.npy', 'rb') as n:
            label = torch.tensor(np.load(n))
        return data, label 

    def __len__(self):
        return len(os.listdir('features'))