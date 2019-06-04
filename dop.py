import os
import cv2
import numpy as np
import pickle

items = {}

for path in os.listdir('/home/afentev/Pictures/datasets/dogs'):
    for file in os.listdir(os.path.join('/home/afentev/Pictures/datasets/dogs', path)):
        file1 = os.path.join('/home/afentev/Pictures/datasets/dogs', path + '/' + file)
        img = np.array(cv2.cvtColor(cv2.imread(file1), cv2.COLOR_BGR2RGB))
        r = round(img[:, :, 0].mean())
        g = round(img[:, :, 1].mean())
        b = round(img[:, :, 2].mean())
        items[file1] = (r, g, b,)

for file in os.listdir('/home/afentev/Pictures/datasets/cats'):
    file1 = os.path.join('/home/afentev/Pictures/datasets/cats', file)
    img = np.array(cv2.cvtColor(cv2.imread(file1), cv2.COLOR_BGR2RGB))
    r = round(img[:, :, 0].mean())
    g = round(img[:, :, 1].mean())
    b = round(img[:, :, 2].mean())
    items[file1] = (r, g, b,)

with open('data.pickle', 'wb') as f:
    pickle.dump(items, f)
