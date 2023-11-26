# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:18:56 2023

@author: M
"""

import streamlit as st
import os

from streamlit_player import st_player
from utils_model.model import SignDetection

SOURCE_LINK = None
VIDEO_PATH = "videos"

TestModel = SignDetection(f"{os.getcwd()}\\utils_model\\best.pt", [], [],\
                          f"{os.getcwd()}\\pngs\\drawable")


def main():

    st.set_page_config(
        page_title="demo",
        page_icon="🚘",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    column1, column2 = st.columns([5, 5])

    try:
        with st.sidebar:
            
            confidence = float(st.sidebar.slider(
                            "Выберите точность", 10, 100, 80)) / 100

            st.title("Выбор видео")
            option = st.radio("Источник", ["Локально (.mp4)", "Youtube"], index=None)

            download_video = st.empty()

            if option == "Локально (.mp4)":
                download_video = st.sidebar.file_uploader(
                    label="Выберите видео", type="mp4", accept_multiple_files=False
                )
                with open(
                    os.path.join(f"{VIDEO_PATH}", download_video.name), "wb"
                ) as f:
                    f.write(download_video.getbuffer())
                    
                with column1:
                    start_local = st.button(label="начать",key = 1, on_click=\
                    TestModel.local_video_processing(VIDEO_PATH, download_video,\
                                                     column2, confidence))

            elif option == "Youtube":
                SOURCE_LINK = st.sidebar.text_input("ссылка на видео YouTube")
                
                with column1:
                    st_player(SOURCE_LINK)
                    start_youtube = st.button(label="начать",key = 2, on_click=\
                    TestModel.ytube_video_processing(SOURCE_LINK, column2, confidence))
            

    except Exception as e:
        st.sidebar.error("Видео не выбрано")


if __name__ == "__main__":
    main()
