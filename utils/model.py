# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:37:49 2023

@author: M
"""
import cv2
import streamlit as st
import pytube as YT
from ultralytics import YOLO


class SignDetection:
    
    def __init__(self, model_path):
        

        self.model = YOLO(model_path)
        
    

    
    def _video_frames(self, st_frame, image):
        
        image = cv2.resize(image, (720, int(720*(9/16))))

        res = self.model.track(image, conf=0.1, persist=True)
        
        res_plotted = res[0].plot()
        st_frame.image(res_plotted,
                       caption='Detected Video',
                       channels="BGR",
                       use_column_width=True
                       )
    
    def key_points(self, path):
        
        results = self.model(path, conf=0.1, stream=False)
        
        for res in results:
            
            print(res.probs)
        
        
        
    
    
    def local_video_processing(self, path, local_video):    

        #with open(f'{path}\\{local_video.name}', 'rb') as video_file:
            #video_bytes = video_file.read()
        
        st.video(local_video)
        
        try:
            vid_cap = cv2.VideoCapture(
                f'{path}\\{local_video.name}')
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    self._video_frames(st_frame, image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Видео не загружено")
            
    
            
    def youtube_video_processing(self, source_link):
        
        
        yt = YT(source_link)
        stream = yt.streams.filter(file_extension="mp4", res=720).first()
        vid_cap = cv2.VideoCapture(stream.url)
        st_frame = st.empty()
        
        while (vid_cap.isOpened()):
            success, image = vid_cap.read()
            if success:
                self._video_frames(st_frame, image)
            else:
                vid_cap.release()
                break
        
            
 # cd Documents\Github\itmo_deep_learning_in_practice           
# streamlit run app.py
            