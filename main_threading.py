# リアルタイムのカメラ画像表示
# threadingを用いた書き方
import threading
import time

import cv2
import streamlit as st
from streamlit import session_state as stss


class Worker(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ret = []
        self.data = []

    def run(self):
        while True:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                self.data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                i = cv2.waitKey(1)
                if i == 27 or i == 13:
                    break
            time.sleep(0.1)


if "worker" not in stss:
    stss.worker = Worker()
    stss.worker.start()

checkbox = st.checkbox("カメラon", value=True)
container = st.empty()

while checkbox:
    container.image(stss.worker.data)
    time.sleep(0.1)
