import cv2 as cv
import numpy as np
import os
dirs = ['soil', 'surface', 'temperature', 'total']


def process():
    for i in range(len(os.listdir('soil'))):
        if i%10 == 0:
            print(i)
        feature_vector = np.array([1,1,1])
        for dir in dirs:
            # print(f'{dir}/{i}.png')
            img = cv.imread(f'{dir}/{i}.png')
            h, w, c = img.shape
            upleft, upright = img[:h//2, :w//2], img[:h//2, w//2:]
            downleft, downright = img[h//2:, :w//2], img[h//2:, w//2:]

            feature_imgs = [upleft, upright, downleft, downright]
            for f_img in feature_imgs:
                three_colors = cv.mean(f_img)[:3]
                feature_vector = np.vstack((feature_vector, three_colors))
        feature_vector = feature_vector[1:]
        feature_vector = feature_vector.flatten()
        with open(f'features/{i}.npy', 'wb') as f:
            np.save(f, feature_vector)