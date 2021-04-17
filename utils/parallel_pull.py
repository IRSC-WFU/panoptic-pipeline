#--------------------------------------------------------------------------------
# This script can pull images and annotations from urls given by the json file
# and save them with the proper format and file name
#-------------------------------------------------------------------------------- 


import json
import requests
import os
import traceback
import multiprocessing
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import rasterio

def read_tiff(filename):
    try:
        # Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
        # Note that for images in the Dark Mining project, we found they use BGRN
        with rasterio.open(filename) as src:
            band_blue_radiance = src.read(1)
            
            band_green_radiance = src.read(2)

            band_red_radiance = src.read(3)

            #band_nir_radiance = src.read(4) # Might be able to remove, since only using RBG bands and not infared

        # Normalizing over 2**12, a value larger than the maximum radiance value in this image
        maxRadiance = np.max([np.max(band_blue_radiance), np.max(band_green_radiance), np.max(band_red_radiance)])
        #img = np.dstack((band_red_radiance, band_green_radiance, band_blue_radiance)) / 2**(np.log2(maxRadiance))
        img = np.dstack((band_blue_radiance, band_green_radiance, band_red_radiance)) / 2**(np.log2(maxRadiance))

        # Scale to 0 - 255
        img = img * 255
        img = img.astype(np.uint8)

        return img
    
    except:
        return -1


def process_image(curr_img_info, curr_run, top_dir, start_idx):
    # pull image
    r = requests.get(curr_img_info['Labeled Data'], stream=True)
    
    #full_image_name = os.path.join(top_dir, curr_run, str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[0]) + str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[1]).lower())
    full_image_name = os.path.join(top_dir, curr_run, str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[0]).replace('_', '-') + '.jpg')

    #handling the tiff input type
    if str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[1]).lower() == '.tif':
        full_image_name = os.path.join(top_dir, curr_run, str(os.path.basename(curr_img_info['Labeled Data'])).replace('_', '-'))

    with open(full_image_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            # writing one chunk at a time to image file 
            if chunk: 
                f.write(chunk)

    curr_id = start_idx

    try:
        #delete tif image if can't be opened 
        if '.tif' in str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[1]).lower():
            temp_img = read_tiff(full_image_name)

            if temp_img is -1:
                os.remove(full_image_name)
                return

            print('Segmenting ' + str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[0]).replace('_', '-') + '.jpg')

            os.remove(full_image_name)

            full_image_name = os.path.join(top_dir, curr_run, str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[0]).replace('_', '-') + '.jpg')
            
            Image.fromarray(temp_img).save(full_image_name)

        else:
            print('Segmenting ' + str(os.path.basename(curr_img_info['Labeled Data'])).replace('_', '-'))

            temp_img = Image.open(full_image_name)

            temp_img = np.array(temp_img)

        try:
            imgName = str(os.path.splitext(os.path.basename(curr_img_info['Labeled Data']))[0]).replace('_', '-')

            list_of_annotations = []
            #read in each annotation images and save them to the right dir with the right format
            for i in range(len(curr_img_info['Label']['objects'])):
                objectName = imgName + '_' + curr_img_info['Label']['objects'][i]['title'] + '_' + str(curr_id)           
                mask_name = os.path.join(top_dir, 'annotations', objectName + '.png')
                mask = requests.get(curr_img_info['Label']['objects'][i]['instanceURI'], stream=True)  
                            
                with open(mask_name, 'wb') as k:
                    for chunk in mask.iter_content(chunk_size=1024): 
                        # writing one chunk at a time to image file 
                        if chunk: 
                            k.write(chunk)

                try:
                    Image.open(mask_name)

                    list_of_annotations.append(mask_name)

                    curr_id+=1
                except:
                    os.remove(mask_name)

            list_of_masks = []

            for i in range(len(list_of_annotations)):
                list_of_masks.append(np.array(Image.open(list_of_annotations[i]).convert('1')))

            list_of_masks = np.array(list_of_masks)
            #removing any intersection among masks
            for i in range(len(list_of_annotations)):
                intersection = list_of_masks.sum(axis=0) > 1

            del list_of_masks

            for i in range(len(list_of_annotations)):
                curr_mask = np.array(Image.open(list_of_annotations[i]).convert('1'))
                curr_mask[intersection] = 0
                
                Image.fromarray(curr_mask).save(list_of_annotations[i])


        except Exception as e:
            print('Error in mask for ' + str(full_image_name))
            print('ID: ' + curr_img_info['ID'])
            print(traceback.format_exc())
            if os.path.isfile(full_image_name):
                os.remove(full_image_name)

    except Exception as e:
            print('Error opening ' + str(full_image_name))
            print('ID: ' + curr_img_info['ID'])
            #print(e)
            print(traceback.format_exc())
                

if __name__ == '__main__':
    curr_run = 'images'
    #curr_info_file = 'info8.json'
    curr_info_file = 'info_fish.json'
    top_dir = os.path.join(os.getcwd(), 'images')
    # Directory Setup
    if not os.path.exists(top_dir):
        os.makedirs(top_dir)
        
    if not os.path.exists(os.path.join(top_dir, 'images')):
        os.makedirs(os.path.join(top_dir, 'images'))

    if not os.path.exists(os.path.join(top_dir, 'annotations')):
        os.makedirs(os.path.join(top_dir, 'annotations'))

    info = json.loads(open(curr_info_file).read())
    
    pool = multiprocessing.Pool() 

    jobs = []

    start_idx = 1
    for curr_img_info in info:
        p = multiprocessing.Process(target = process_image, args=(curr_img_info, curr_run, top_dir, start_idx))
        jobs.append(p)
        p.start()
        if len(curr_img_info['Label']) != 0:
            start_idx+=len(curr_img_info['Label']['objects'])
    
    cat = list(set([i.split('_')[1] for i in os.listdir(os.path.join(top_dir, 'annotations'))]))
    print(cat)