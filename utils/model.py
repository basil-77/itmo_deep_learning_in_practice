# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 17:37:49 2023

@author: M
"""
import cv2
import streamlit as st

from ultralytics import YOLO




def load_model(model_path):
    
    model = YOLO(model_path)
    return model

    
def _video_frames(model, st_frame, image):
    

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Display object tracking, if specified
    res = model.track(image, conf=0.1, persist=True)
    
    # # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )
    
def local_video_processing(path, local_video, model):    

    with open(f'{path}\\{local_video.name}', 'rb') as video_file:
        video_bytes = video_file.read()
    
    st.video(local_video)
    
    try:
        vid_cap = cv2.VideoCapture(
            f'{path}\\{local_video.name}')
        st_frame = st.empty()
        while (vid_cap.isOpened()):
            success, image = vid_cap.read()
            if success:
                _video_frames(model, st_frame, image)
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.sidebar.error("Error loading video: " + str(e))