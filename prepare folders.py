# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 20:45:55 2023

@author: M
"""
import sys
import os
from ultralytics import YOLO
from shutil import copyfile, move, copy
from JSON2YOLO.general_json2yolo import convert_coco_json
from tqdm.notebook import tqdm


# =============================================================================
# with open('JSON2YOLO\\general_json2yolo.py', 'r+') as fd:
#     lines = fd.readlines()                                                     
#     fd.seek(0)                                                                 
#     line273 = ["            h, w, f = img['height'], img['width'], img['file_name'].split('/')[1]"]
#     print(line273)
#     fd.writelines(lines[:273] + line273 + lines[274:])
# =============================================================================

fd = open('JSON2YOLO\\general_json2yolo.py', 'r')                                             
lines = fd.readlines()                                                     
fd.seek(0)                                                                 
print(lines[273])
fd.close()

sys.path.append('\\archive')
sys.path.append('\\JSON2YOLO')


test_path = '.\\test_annotation'
train_path = '.\\train_annotation'

os.makedirs(train_path, exist_ok=True)
os.makedirs(test_path, exist_ok=True)

copy('archive\\train_anno.json', os.path.join(train_path, 'train_anno.json'))
copy('archive\\val_anno.json', os.path.join(test_path, 'val_anno.json'))

for folder in ['labels', 'images']:
    for path in [test_path, train_path]:
        os.makedirs(os.path.join(path, folder), exist_ok=True)
        
convert_coco_json(train_path)
for file in tqdm(os.listdir(os.path.join('new_dir\\labels\\train_anno'))):
    move(os.path.join('new_dir\\labels\\train_anno', file), os.path.join(train_path, 'labels', file))
    
convert_coco_json('.\\test_annotation\\')
for file in tqdm(os.listdir(os.path.join('new_dir\\labels\\val_anno'))):
    move(os.path.join('new_dir\\labels\\val_anno', file), os.path.join(test_path, 'labels', file))
    
    
##############################################################################################################
#Images
#
#


test_labels = os.listdir(os.path.join(test_path, 'labels'))
train_labels = os.listdir(os.path.join(train_path, 'labels'))

test_labels = set(map(lambda x: x.split('.')[0], test_labels))
train_labels = set(map(lambda x: x.split('.')[0], train_labels))

images = 'archive\\rtsd-frames\\rtsd-frames'
for file in os.listdir(images):
    name = file.split('.')[0]
    if name in train_labels:
        copy(os.path.join(images, file), os.path.join(train_path,'images', file))
    if name in test_labels:
        copy(os.path.join(images, file), os.path.join(test_path,'images', file))

