# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:18:56 2023

@author: M
"""

import streamlit as st
import pytube as YT
import os

from streamlit_player import st_player
from utils.model import load_model, local_video_processing

SOURCE_LINK = None 
VIDEO_PATH = 'videos'

Test_model = load_model(f'{os.getcwd()}\\utils\\yolov8n.pt')

def main():
    
    st.set_page_config(page_title="demo",
                       page_icon="🚘",
                       layout="wide",
                       initial_sidebar_state="expanded")
    
    column1, column2 = st.columns([5,5])
    
    
    

    with st.sidebar:
        
        st.title("Выбор видео")
        option = st.radio("Источник",
                              ["Локально (.mp4)", "Youtube"],
                              index=None)
        
        download_video=st.empty()
        
        if option == 'Локально (.mp4)':
            download_video = st.sidebar.file_uploader(label="Выберите видео",\
                                                      type='mp4',\
                                                      accept_multiple_files=False)
            with open(os.path.join(f'{VIDEO_PATH}', download_video.name),"wb") as f:
                      f.write(download_video.getbuffer())
                      
        elif option == 'Youtube':
            SOURCE_LINK = st.sidebar.text_input("ссылка на видео YouTube")
            
    
    with column1:
        try:    
            if download_video:
                local_video_processing(VIDEO_PATH, download_video, Test_model)
                column2.write('')
            if SOURCE_LINK:
                st_player(SOURCE_LINK)
        except Exception as e:
            st.sidebar.error("Видео не выбрано")



    

if __name__ == "__main__":
    main()