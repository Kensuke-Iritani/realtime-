# 最もシンプルな書き方
# チェックボックス押下直後に動作が固まる以外はいい感じ
import cv2
import streamlit as st

cap = cv2.VideoCapture(0)

bool_ = st.checkbox("カメラon", value=True)
container = st.empty()

while bool_:
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        container.image(frame)
        i = cv2.waitKey(1)
        if i == 27 or i == 13:
            break
