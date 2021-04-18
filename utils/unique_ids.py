import argparse
import os

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-d","--directory",dest="directory",help="Directory Name", default='images/annotations')
    args = parse.parse_args()

    id_list = []

    for curr in os.listdir(args.directory):
        id_list.append(int(os.path.splitext(curr)[0].split('_')[-1]))

    print('Unique IDs?', len(list(set(id_list)))==len(id_list))
