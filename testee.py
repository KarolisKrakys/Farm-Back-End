import numpy as np
import torch
import cv2 as cv

from feature import process
from model import NeuralNetwork


outputs = [0.2,0.6,0.1, 0.3]
blank_image = np.zeros((64, 64, 3), dtype=np.uint8)
if outputs[0] < 0.5:
    blank_image[:32, :32] = (0,0,255)
else:
    blank_image[:32, :32] = (0,255, 0)
if outputs[1] < 0.5:
    blank_image[:32, 32:] = (0,0,255)
else:
    blank_image[:32, 32:] = (0,255, 0)
if outputs[2] < 0.5:
    blank_image[32:, :32] = (0,0,255)
else:
    blank_image[32:, 32:] = (0,255, 0)
if outputs[3] < 0.5:
    blank_image[32:, 32:] = (0,0,255)
else:
    blank_image[32:, 32:] = (0,255, 0)
cv.imshow('test', blank_image) 
cv.imwrite('see.jpg', blank_image)