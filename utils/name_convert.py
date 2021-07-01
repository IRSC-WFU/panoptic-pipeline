import os

import argparse

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-b","--base",dest="base",help="Base directory", default='data')
    parse.add_argument("-g","--group",dest="group",help="train, val, or test", default='train')
    args = parse.parse_args()

    topdir = os.path.join(args.base, args.group)

    for directory in [os.path.join(topdir, i) for i in ['images', 'annotations']]:
        for file in os.listdir(directory):
            new_name = file.replace('(', '-').replace(')', '-')

            os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
