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

    def _video_frames(self, st_frame, image, flag, column):

        if not flag:

            image = cv2.resize(image, (720, int(720 * (9 / 16))))

            res = self.model.track(image, conf=0.2, persist=True)

            res_str = res[0].verbose()

            res_plotted = res[0].plot()

            with column:

                if res_str != "(no detections), ":
                    st.write(res_str)
                    st.image(res_plotted, caption="Распознано", use_column_width=True)
                else:
                    pass

            st_frame.image(
                res_plotted, caption="Tracking", channels="BGR", use_column_width=True
            )
        else:

            image.release()

    def local_video_processing(self, path, local_video, column):

        st.video(local_video)

        flag = st.button(label="остановить")
        try:
            vid_cap = cv2.VideoCapture(f"{path}\\{local_video.name}")
            st_frame = st.empty()

            while not flag:
                success, image = vid_cap.read()
                if success:
                    self._video_frames(st_frame, image, flag, column)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Видео не загружено")


# cd Documents\Github\itmo_deep_learning_in_practice
# streamlit run app.py
