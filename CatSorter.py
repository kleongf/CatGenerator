# the cats in the dataset have different colors
# i want to be able to sort by each color to reduce confusion
# main cat colors identified:
# white, black
# gray
# yellow/brown ish

import cv2
import numpy as np
import os
import pandas as pd

path = '/Users/kevin/HolyShitCatGenerator/cats2'
lst = os.listdir(path)

# Expanded HSV range for black
lower_black = (0, 0, 0)          # Very low Hue, Saturation, and Value
upper_black = (180, 70, 70)      # Increased Saturation and Value to allow for dark grays

# Expanded HSV range for white
lower_white = (0, 0, 200)        # Low Saturation, high Value
upper_white = (180, 60, 255)     # Slightly higher Saturation and full Value

# Restricted HSV range for gray
lower_gray = (0, 0, 80)          # Low Saturation, slightly darker Value
upper_gray = (180, 40, 200)      # Still low Saturation, medium Value

# Expanded HSV range for yellow/gold
lower_yellow = (20, 120, 120)    # Lower Saturation and Value for darker yellows
upper_yellow = (40, 255, 255)    # Full Saturation and Value

colors = [[lower_black, upper_black], [lower_white, upper_white], [lower_gray, upper_gray], [lower_yellow, upper_yellow]]

def process_image(file_name):
    image_path = os.path.join(path, file_name)
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    color_values = []
    for color in colors:
        mask = cv2.inRange(hsv, color[0], color[1])
        count = np.count_nonzero(mask)
        color_values.append(count)

    return color_values.index(max(color_values))
    # get index of max value and map it to a color later

data = [[fname, process_image(fname)] for fname in lst]
df = pd.DataFrame(data, columns=['filename', 'value'])
df.to_csv('SortedLabels2.csv', index=False)