# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 23:59:38 2023

@author: M
"""

from ultralytics import YOLO

model = YOLO('.\\yolov8n.pt')


data_yaml = 'trafic_signs.yaml'

def main():
    
    model.train(data=data_yaml, epochs=20, batch=10, imgsz=1280, device='0')

if __name__ == '__main__':
    main()

