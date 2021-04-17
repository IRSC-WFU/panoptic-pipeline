import random
from PIL import Image, ImageDraw
import math
import os
import numpy as np

def name2color(name):
    if name == 'triangle':
        return (255,0,0)
    if name == 'rectangle':
        return (0,0,255)
    if name == 'circle':
        return (128,0,128)
    if name == 'shape':
        return (255,255,0)
    if name == 'shape1':
        return (0,255,0)
    if name == 'shape2':
        return (0,128,255)

if __name__ == '__main__':
    
    ROOT_DIR = '/deac/generalGrp/paucaGrp/dark_mining/Panoptic-Segmentation-for-Dark-Mining/images'
    IMAGE_DIR = os.path.join(ROOT_DIR, "images")
    ANNOTATION_DIR = os.path.join(ROOT_DIR, "annotations")

    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)
        
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    if not os.path.exists(ANNOTATION_DIR):
        os.makedirs(ANNOTATION_DIR)

    
    curr_id = 1
    for number in range(50):
        img = Image.new("RGB", (500,500), color='white')
        img1 = ImageDraw.Draw(img)  
        name = 'img' + str(number) + '.png'
        rangeNum = 1
        trinum = random.randint(1,rangeNum)
        rectNum = random.randint(1,rangeNum)
        ovalNum = random.randint(1,rangeNum)
        pentNum = random.randint(1,rangeNum)
        vertices = []
        for tri in range(trinum):
            tritem = []
            for k in range(3):                         # Do this 3 times
                x = random.randint(0, 150)             # Create a random x value
                y = random.randint(0, 150)             # Create a random y value
                # vertices.append((x,y))  # Add the (x, y) point to the vertices
                tritem.append((x,y))
            img1.polygon(tritem, fill =name2color('triangle')) 


        for rect in range(rectNum):
            recttem = []
            for k in range(2):                         # Do this 3 times
                x = random.randint(150, 300)             # Create a random x value
                y = random.randint(0, 150)             # Create a random y value
                recttem.append((x,y))
            x1 = recttem[0][0]
            y1 = recttem[1][1]
            x2 = recttem[1][0]
            y2 = recttem[0][1]
            recttem.append((x2,y2))
            recttem.append((x1,y1))
            a = recttem[1]
            recttem[1] = recttem[2]
            recttem[2] = a
            img1.polygon(recttem, fill =name2color('rectangle')) 


        for cir in range(ovalNum):
            x = random.randint(0, 200)            
            y = random.randint(200, 250)
            r = random.randint(15,60)
            img1.ellipse((x-r, y-r, x+r, y+r), fill =name2color('circle'))
            
        for shape in range(pentNum):
            side = 8
            location1 = random.randint(0, 200) 
            location2 = random.randint(300, 450) 
            size = random.uniform(0.5, 1.0)
            xy = [
                (     (math.cos(th) + 1) * 90 * size + location1,     (math.sin(th) + 1) * 60  * size + location2    )
                for th in [i * (2 * math.pi) / side for i in range(side)]
                ]   
            img1.polygon(xy, fill =name2color('shape'))

        for shape in range(pentNum):
            side = 6
            location1 = random.randint(300, 500) 
            location2 = random.randint(150, 250) 
            size = random.uniform(0.3, 0.8)
            xy = [
                (     (math.cos(th) + 1) * 90 * size + location1,     (math.sin(th) + 1) * 60  * size + location2    )
                for th in [i * (2 * math.pi) / side for i in range(side)]
                ]   
            img1.polygon(xy, fill =name2color('shape2'))


        for shape in range(pentNum):
            side = 5
            location1 = random.randint(300, 500) 
            location2 = random.randint(400, 450) 
            size = random.uniform(0.3, 0.8)
            xy = [
                (     (math.cos(th) + 1) * 90 * size + location1,     (math.sin(th) + 1) * 60  * size + location2    )
                for th in [i * (2 * math.pi) / side for i in range(side)]
                ]   
            img1.polygon(xy, fill =name2color('shape1'))

        img.save(os.path.join(IMAGE_DIR,name))
        rectName = 'img' + str(number) + '_tri_' + str(curr_id) +'.png'
        npImage=np.array(img)
        mask = np.zeros([500,500],dtype=np.uint8)
        mask[np.where(np.all(npImage==(255,0,0),axis=2))] = 255
        result=Image.fromarray(mask)
        result.save(os.path.join(ANNOTATION_DIR,rectName))
        curr_id += 1

        rectName = 'img' + str(number) + '_rect_' + str(curr_id) +'.png'
        npImage=np.array(img)
        mask = np.zeros([500,500],dtype=np.uint8)
        mask[np.where(np.all(npImage==[0,0,255],axis=2))] = 255
        result=Image.fromarray(mask)
        result.save(os.path.join(ANNOTATION_DIR,rectName))
        curr_id += 1

        rectName = 'img' + str(number) + '_circle_' + str(curr_id) +'.png'
        npImage=np.array(img)
        mask = np.zeros([500,500],dtype=np.uint8)
        mask[np.where(np.all(npImage==[128,0,128],axis=2))] = 255            
        result=Image.fromarray(mask)
        result.save(os.path.join(ANNOTATION_DIR,rectName))
        curr_id += 1


        rectName = 'img' + str(number) + '_shape_' + str(curr_id) +'.png'
        npImage=np.array(img)
        mask = np.zeros([500,500],dtype=np.uint8)
        mask[np.where(np.all(npImage==[255,255,0],axis=2))] = 255
        result=Image.fromarray(mask)
        result.save(os.path.join(ANNOTATION_DIR,rectName))
        curr_id += 1

        rectName = 'img' + str(number) + '_shape1_' + str(curr_id) +'.png'
        npImage=np.array(img)
        mask = np.zeros([500,500],dtype=np.uint8)
        mask[np.where(np.all(npImage==name2color('shape1'),axis=2))] = 255
        result=Image.fromarray(mask)
        result.save(os.path.join(ANNOTATION_DIR,rectName))
        curr_id += 1

        rectName = 'img' + str(number) + '_shape2_' + str(curr_id) +'.png'
        npImage=np.array(img)
        mask = np.zeros([500,500],dtype=np.uint8)
        mask[np.where(np.all(npImage==name2color('shape2'),axis=2))] = 255
        result=Image.fromarray(mask)
        result.save(os.path.join(ANNOTATION_DIR,rectName))
        curr_id += 1

        rectName = 'img' + str(number) + '_stuff_' + str(curr_id) +'.png'
        npImage=np.array(img)
        mask = np.zeros([500,500],dtype=np.uint8)
        mask[np.where(np.all(npImage==[255,255,255],axis=2))] = 255
        result=Image.fromarray(mask)
        result.save(os.path.join(ANNOTATION_DIR,rectName))
        curr_id += 1
        