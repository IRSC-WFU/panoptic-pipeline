import os
import json
import re

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import seaborn as sns

BASE_DIR = 'images'

with open('panoptic_coco_categories.json', 'r') as f:
    CATEGORIES = json.load(f)

cat_list = [x['name'] for x in CATEGORIES]

img_list = [os.path.splitext(i)[0] for i in os.listdir(os.path.join(BASE_DIR, 'images'))]

data_dict = {'Image' : img_list}

for c in cat_list:
    data_dict[c] = [0]*len(img_list)
    for i in range(len(img_list)):
        for ann in os.listdir(os.path.join(BASE_DIR, 'annotations')):
            if (img_list[i] in ann) and (c in ann):
                data_dict[c][i]+=1

df = pd.DataFrame.from_dict(data_dict)
img_list = list(df['Image'].values)
df = df.set_index('Image')

plt.figure(figsize=(10, 12))

ax = sns.heatmap(df, xticklabels=True, yticklabels=True, annot=True, linewidths=.5, annot_kws={"size": 10}, cmap="YlGnBu")
rot = 45
ax.set_xticklabels(rotation=rot, labels=cat_list)
ax.set_yticklabels(labels=img_list)
plt.title('Class Map Per Image')

plt.savefig('class_map.png')
