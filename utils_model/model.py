# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:37:49 2023

@author: M
"""
import cv2
import os
import streamlit as st
import torch

from PIL import Image
from pytube import YouTube
from ultralytics import YOLO



class SignDetection:
    def __init__(self, model_path, arr, sc, path):

        self.model = YOLO(model_path)
        self.detected_frames = arr
        self.detected_scores = sc
        self.path = path
        if torch.cuda.is_available():
            self.cuda = torch.cuda.current_device()
            print(f'use cuda device:{torch.cuda.get_device_name(self.cuda)}')
        else:
            self.cuda = 'cpu'
            print('cant use cuda')
        
    def get_sign(self, sign_id):
      
        dir_path = self.path
        size = 128, 128
        
        try:
            img = Image.open(f'{dir_path}\\znak_{sign_id}.png')
            img.thumbnail(size)  
        except Exception as e:
            img = Image.open(f'{dir_path}\\none.png')
            img.thumbnail(size)  
       
        return img
                 
            
    def _video_frames(self, st_frame, image, flag, column, conf):

        if not flag:

            image = cv2.resize(image, (720, int(720 * (9 / 16))))
            
            
            res = self.model.track(image, conf=conf, persist=True, device=self.cuda)

            res_str = res[0].verbose()
            
            keys = res[0].boxes
            
            names = res[0].names
            
            res_plotted = res[0].plot()

            with column:
                
                if res_str != "(no detections), " and res_str not in self.detected_frames:
                    self.detected_frames.append(f'{res_str}')
                    self.detected_scores.append(f'{keys.conf.item():.2f}')
                    st.write(res_str, f'{keys.conf.item():.2f}')
                    st.image(self.get_sign(res_str.split()[1][:-1]))
                    st.image(res_plotted, caption="Распознано", use_column_width=True)
                else:
                    pass

            st_frame.image(
                res_plotted, caption="Tracking", channels="BGR", use_column_width=True
            )
        else:

            image.release()

    def local_video_processing(self, path, local_video, column, conf):

        st.video(local_video)

        flag = st.button(label="остановить")
        try:
            vid_cap = cv2.VideoCapture(f"{path}\\{local_video.name}")
            st_frame = st.empty()

            while not flag:
                success, image = vid_cap.read()
                if success:
                    self._video_frames(st_frame, image, flag, column, conf)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Видео не загружено")
            
    def ytube_video_processing(self, link, column, conf):

        flag = st.button(label="остановить")
       
        try:
            yt = YouTube(link)
            stream = yt.streams.filter(file_extension="mp4", res=720).first()
            vid_cap = cv2.VideoCapture(stream.url)
            st_frame = st.empty()

            while not flag:
                success, image = vid_cap.read()
                if success:
                    self._video_frames(st_frame, image, flag, column, conf)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Видео не загружено")


# cd Documents\Github\itmo_deep_learning_in_practice
# streamlit run app.py
