import os
import json
import re

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import seaborn as sns

def pull_cm(filename):
    with open(filename, 'r') as f:
        content = f.read()
    regex = re.compile('(confusion_matrix:\n\d+-\d+-\d+ \d+:\d+:\d+,\d+ \| coco.py    \| line \d+?: ((\d+.\d*?(\s|\n)*)+))')
    found_vals = regex.findall(content)
    return found_vals[0][1]

def pull_pq(filename):
    with open(filename, 'r') as f:
        content = f.read()

    unified = '\d+-\d+-\d+ \d+:\d+:\d+,\d+ \| base_dataset.py \| line \d+?:\s*(\d+)\s+\|\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)\s+(\d+)\s+(\d+)\n'
    regex = re.compile('(' + unified + ')')
    found_vals = regex.findall(content)

    metrics = {}

    for curr in found_vals:
        metrics[curr[1]] = [curr[i] for i in range(2,9)]

    df = pd.DataFrame.from_dict(metrics, orient = 'index', columns=['PQ', 'SQ', 'RQ', 'IoU', 'TP', 'FP', 'FN'])
    return df

def pull_full_pq(filename):
    with open(filename, 'r') as f:
        content = f.read()

    unified = '\d+-\d+-\d+ \d+:\d+:\d+,\d+ \| base_dataset.py \| line \d+?: (\w+)\s+\|\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+)\n'
    regex = re.compile('(' + unified + ')')
    found_vals = regex.findall(content)

    metrics = {}

    for curr in found_vals:
        metrics[curr[1]] = [curr[2], curr[3], curr[4], curr[5]]

    df = pd.DataFrame.from_dict(metrics, orient = 'index', columns=['PQ', 'SQ', 'RQ', 'N'])
    return df
    
'''
2021-04-14 06:47:15,067 | coco.py    | line 266: IU_array:
2021-04-14 06:47:15,067 | coco.py    | line 268: 0.80758
2021-04-14 06:47:15,067 | coco.py    | line 268: 0.61407
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.00000
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.91046
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.91289
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.61051
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.00000
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.40115
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.38962
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.00000
2021-04-14 06:47:15,068 | coco.py    | line 268: 0.46774'''

def pull_IU(filename,n):
    with open(filename, 'r') as f:
        content = f.read()

    header =  '\d+-\d+-\d+ \d+:\d+:\d+,\d+ \| coco.py    \| line \d+?: IU_array:\n'
    unified = '\d+-\d+-\d+ \d+:\d+:\d+,\d+ \| coco.py    \| line \d+?: (\d+\.\d+)'
    regex = re.compile('(' + unified + ')+')
    found_vals = regex.findall(content)
    values = []
    for i in range(n):
        values.append(found_vals[i][1])

    return values


if __name__ == '__main__':
    filename = '/deac/generalGrp/paucaGrp/dark_mining/UPSNet/output/upsnet/mining_resnet101/upsnet_resnet101_mine_2gpu/val2017/upsnet_resnet101_mine_2gpu_2021-04-14-06-46.log'
    top_dir = os.path.join(os.getcwd(), 'graphics')
    catfile = '/deac/generalGrp/paucaGrp/dark_mining/UPSNet/data/coco/annotations/panoptic_coco_categories_stff.json'

    if not os.path.exists(top_dir):
        os.makedirs(top_dir)

    # Generate Confusion Matrix Plot
    print('Generating Confusion Matrix Plot')
    input_str = pull_cm(filename)

    with open(os.path.join(top_dir, 'temp_cm_text.txt'), 'w') as f:
        f.write(input_str)

    cm = np.genfromtxt(os.path.join(top_dir, 'temp_cm_text.txt'), dtype=np.float32, delimiter='\t')

    with open(catfile, 'r') as f:
        CATEGORIES = json.load(f)
        cat_dict = {}

    for i in range(len(CATEGORIES)):
        cat_dict[i] = [j['name'] for j in CATEGORIES if j['id'] == i][0]

    os.remove(os.path.join(top_dir, 'temp_cm_text.txt'))

    df = pd.DataFrame(cm)
    df.index = [cat_dict[i] for i in df.index]
    df.columns = [cat_dict[i] for i in df.columns]

    fig = plt.figure(figsize=(15,10))

    sns.set(font_scale = 1.2)
    ax = sns.heatmap(df, annot=True, annot_kws={"size": 12}, robust=True, cmap='Blues')

    ax.set_xticklabels(rotation=70, labels=df.columns)
    ax.tick_params(axis="x", bottom=True)
    ax.tick_params(axis="y", left=True)
    ax.set_ylabel('Actual')
    ax.set_xlabel('Predicted')
    ax.set_title('UPSNet Confusion Matrix (Normalized Over True Labels)', fontsize=20, pad=20)

    plt.tight_layout()

    plt.savefig(os.path.join(top_dir, 'confusion_matrix.png'))
    plt.close()

    # Generate Full PQ Plot
    print('Generating Averaged PQ, SQ, RQ, N Plot')
    full_pq_df = pull_full_pq(filename)

    fig, axs = plt.subplots(2, 2, figsize=(15,12))

    cats = full_pq_df.index
    rot = 60

    sns.barplot(x=cats, y=np.array(full_pq_df['PQ'], dtype=np.float32), ax=axs[0, 0])
    axs[0, 0].set_title('PQ', fontsize=20, pad=20)
    axs[0, 0].set_xticklabels(rotation=rot, labels=cats)

    ax = sns.barplot(x=cats, y=np.array(full_pq_df['SQ'], dtype=np.float32), ax=axs[0, 1])
    axs[0, 1].set_title('SQ', fontsize=20, pad=20)
    axs[0, 1].set_xticklabels(rotation=rot, labels=cats)

    ax = sns.barplot(x=cats, y=np.array(full_pq_df['RQ'], dtype=np.float32), ax=axs[1, 0])
    axs[1, 0].set_title('RQ', fontsize=20, pad=20)
    axs[1, 0].set_xticklabels(rotation=rot, labels=cats)

    ax = sns.barplot(x=cats, y=np.array(full_pq_df['N'], dtype=np.float32), ax=axs[1, 1])
    axs[1, 1].set_title('Number of Categories', fontsize=20, pad=20)
    axs[1, 1].set_xticklabels(rotation=rot, labels=cats)

    fig.suptitle('Average PQ, SQ, RQ, and Category Count', fontsize=25)

    plt.tight_layout()

    plt.savefig(os.path.join(top_dir, 'averaged_metrics.png'))
    plt.close()

    # Generate Category PQ, SQ, RQ, IoU Plot
    print('Generating Category PQ, SQ, RQ, IoU Plot')
    cat_pq_df = pull_pq(filename)

    fig, axs = plt.subplots(2, 2, figsize=(15,12))

    cats = [cat_dict[int(i)] for i in cat_pq_df.index]
    rot = 60

    sns.barplot(x=cats, y=np.array(cat_pq_df['PQ'], dtype=np.float32), ax=axs[0, 0])
    axs[0, 0].set_title('PQ', fontsize=20, pad=20)
    axs[0, 0].set_xticklabels(rotation=rot, labels=cats)

    ax = sns.barplot(x=cats, y=np.array(cat_pq_df['SQ'], dtype=np.float32), ax=axs[0, 1])
    axs[0, 1].set_title('SQ', fontsize=20, pad=20)
    axs[0, 1].set_xticklabels(rotation=rot, labels=cats)

    ax = sns.barplot(x=cats, y=np.array(cat_pq_df['RQ'], dtype=np.float32), ax=axs[1, 0])
    axs[1, 0].set_title('RQ', fontsize=20, pad=20)
    axs[1, 0].set_xticklabels(rotation=rot, labels=cats)

    ax = sns.barplot(x=cats, y=np.array(cat_pq_df['IoU'], dtype=np.float32), ax=axs[1, 1])
    axs[1, 1].set_title('IoU', fontsize=20, pad=20)
    axs[1, 1].set_xticklabels(rotation=rot, labels=cats)

    fig.suptitle('Per-Category PQ, SQ, RQ, and IoU', fontsize=25)

    plt.tight_layout()

    plt.savefig(os.path.join(top_dir, 'cat_metrics_plot.png'))
    plt.close()


    # Generate IU
    print('Generating IU Plot')
    iu = pull_IU(filename, int(full_pq_df['N'].loc['All']))
    ax = sns.barplot(x=[cat_dict[int(i)] for i in range(int(full_pq_df['N'].loc['All']))], y=np.array(iu, dtype=np.float32))

    ax.set_title('IU')
    ax.set_ylabel('IU')
    ax.set_xlabel('Class')

    ax.set_xticklabels(rotation=75, labels=[cat_dict[int(i)] for i in range(int(full_pq_df['N'].loc['All']))])
    ax.tick_params(axis="x", bottom=True)
    ax.tick_params(axis="y", left=True)

    plt.tight_layout()

    plt.savefig(os.path.join(top_dir, 'iu_plot.png'))
    plt.close()
