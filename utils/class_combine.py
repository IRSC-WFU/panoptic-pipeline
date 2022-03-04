import os

import argparse

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("-b","--base",dest="base",help="Base directory", default='images/annotations')
    args = parse.parse_args()

    directory = args.base

    swap_dict = {
                    "Pozas de minería" : "mining-pond",
                    "Relaves" : "tailing",
                    "Tolvas" : "equipment",
                    "intact-forest" : "forest",
                    "float" : "equipment",
                    "Campamento minero intacto" : "building",
                    "small-vegetation" : "vegetation",
                    "Excavadoras" : "vehicle",
                    "remnent-forest" : "forest",
                    "Vehículos pequeños" : "vehicle",
                    "Suelo desnudo" : "ground",
                    "river" : "river",
                    "Carreteras" : "ground",
                    "dredge" : "equipment",
                    "Árboles y bosque" : "forest",
                    "Camiones volquete grandes" : "vehicle",
                    "Chute" : "equipment",
                    "large-tailing" : "ground",
                    "Cargador frontal" : "vehicle",
                    "Campamento minero destruido" : "building",
                    "Edificios" : "building",
                    "small-building" : "building",
                    "Vegetación pequeña" : "vegetation",
                    "Tubos - Mangueras" : "equipment",
                    "Balsas de mineria intactas" : "equipment"
                }

    for file in os.listdir(directory):
        new_name = file.replace('(', '-').replace(')', '-')

        for key, value in swap_dict.items():
            new_name = new_name.replace(key, value)

        os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
