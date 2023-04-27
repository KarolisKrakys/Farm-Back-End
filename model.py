from cProfile import label
import os
import torch
from torch.nn import Module, Sequential, Linear, ReLU, BatchNorm1d, Sigmoid, Dropout, Conv1d
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from dataset import featureDataset
import matplotlib.pyplot as plt


BATCH_SIZE = 60

'''
1D Convolutional model
'''

class NeuralNetwork(Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.linear_relu_stack = Sequential(
            Conv1d(1, 16, 4, stride=3),
            ReLU(),
            Conv1d(16, 32, 4, stride=3),
            ReLU()
        )
        self.part2  = Sequential(
            Linear(7680, 128),
            ReLU(),
            Dropout(0.4),
            Linear(128, 64),
            ReLU(),
            Linear(64, BATCH_SIZE)
        )
    
    def forward(self, x):
        x = self.linear_relu_stack(x)
        x = x.flatten()
        output = self.part2(x)
        # print(f'output shape is {output.size()}')
        return output.unsqueeze(1)