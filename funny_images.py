import os
import cv2
import pickle
import numpy as np
from math import sqrt


def lost_function(r_segm, g_segm, b_segm, arg):
    """Можно еще такое попробовать*
    ColorDelta = dR + dG + dB
    ColorDelta = sqrt(dR*dR*0.2126 + dG*dG*0.7152 + dB*dB*0.0722)
    ColorDelta = sqrt(dR*dR*0.2126*0.2126 + dG*dG*0.7152*0.7152 + dB*dB*0.0722*0.0722)
    """
    r, g, b = arg[1]
    return sqrt((r - r_segm) ** 2 + (g - g_segm) ** 2 + (b - b_segm) ** 2)


PATH_TO_PICTURE = '/home/afentev/Pictures'
PICTURE = 'лиза.jpg'

VERTICAL_SECTION_SIZE = 6
HORIZONTAL_SECTION_SIZE = 6

with open('data.pickle', 'rb') as f:
    items = pickle.load(f)

file = os.path.join(PATH_TO_PICTURE, PICTURE)
img = np.array(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB))
size = img.shape
x, y = size[0], size[1]
img = cv2.resize(img, (y - (y % VERTICAL_SECTION_SIZE), x - (x % HORIZONTAL_SECTION_SIZE)))
size = img.shape
x, y = size[0], size[1]
q = 1
tot = (x // HORIZONTAL_SECTION_SIZE) * (y // VERTICAL_SECTION_SIZE)
for i in range(x // HORIZONTAL_SECTION_SIZE):
    for j in range(y // VERTICAL_SECTION_SIZE):
        sect = img[i * HORIZONTAL_SECTION_SIZE:(i + 1) * HORIZONTAL_SECTION_SIZE,
                j * VERTICAL_SECTION_SIZE:(j + 1) * VERTICAL_SECTION_SIZE]
        r_mean, g_mean, b_mean = sect[:, :, 0].mean(), sect[:, :, 1].mean(), sect[:, :, 2].mean()
        current = sorted(items.items(), key=lambda argument: lost_function(r_mean, g_mean, b_mean, argument))[0]
        resized = cv2.resize(cv2.cvtColor(cv2.imread(current[0]), cv2.COLOR_BGR2RGB),
                             (VERTICAL_SECTION_SIZE, HORIZONTAL_SECTION_SIZE,))
        img[i * HORIZONTAL_SECTION_SIZE:(i + 1) * HORIZONTAL_SECTION_SIZE,
        j * VERTICAL_SECTION_SIZE:(j + 1) * VERTICAL_SECTION_SIZE] = resized
        print(q / tot)
        q += 1
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
cv2.imshow('ImageWindow', img)
cv2.waitKey(0)
