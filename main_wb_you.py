# asyncioを用いて並列処理化
# サクサク動く感じになった
# cv2.VideoCapture(0)を起動時に読み込むようにしたのが大きそう
# 簡易的な移動検出（背景差分抽出）の処理を追加
# 録画機能（UIのみ）を追加

import asyncio
import time

import cv2
import mss
import numpy as np
import streamlit as st
from streamlit import session_state as stss

from utils.image_processing import add_cursor, bin_partly, motion_detection
from utils.texts import ABSTRACT, HIDE_ST_STYLE

# ページ全体の設定
st.set_page_config(
    page_title="Real-Time Image Processing",
    page_icon="🎞️",
    # layout="wide",
)

# メニューバーを非表示にする
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)  # HIDE_ST_STYLEを適用

# セッション状態の初期化
if "frame" not in stss:
    stss.frame = None
if "switch" not in stss:
    stss.switch = "カメラ"
if "method" not in stss:
    stss.method = "無加工"
if "threshold" not in stss:
    stss.threshold = [100, 150]
if "cap" not in stss:
    stss.cap = cv2.VideoCapture(0)
if "fgbg" not in stss:
    stss.fgbg = cv2.createBackgroundSubtractorMOG2(
        history=100, varThreshold=50, detectShadows=False
    )
if "rec_status" not in stss:
    stss.rec_status = 0
    stss.rec_start = 0
    stss.rec_time = 5


async def main():
    st.header("リアルタイム画像処理", divider="gray")
    frame_container = st.empty()
    with st.expander("See explanation"):
        st.markdown(ABSTRACT)
    set_widgets(st.sidebar)

    tasks = []
    tasks += [asyncio.create_task(toast())]
    tasks += [asyncio.create_task(recording_countdown())]
    tasks += [asyncio.create_task(set_camera_image())]
    tasks += [asyncio.create_task(set_screen())]
    tasks += [asyncio.create_task(disp_frame(frame_container))]
    await asyncio.gather(*tasks)
    # stss.cap.release()


def rec_start():
    stss.rec_status = 1


def rec_stop():
    stss.rec_status = 4


def set_widgets(area):
    # レイアウト
    area.subheader("画像処理")
    switch_container, method_container = area.columns(2)
    slider_container = area.empty()
    area.markdown("---")
    area.subheader("録画")
    length_container = area.empty()
    rec_container = area.empty()

    # ウィジェット
    stss.switch = switch_container.radio(
        "処理対象", ["カメラ", "スクリーン"], disabled=bool(stss.rec_status)
    )
    stss.rec_time = length_container.slider(
        "録画時間", min_value=1, max_value=10, value=5, step=1
    )
    rec_container.button("録画開始", disabled=bool(stss.rec_status), on_click=rec_start)
    if stss.rec_status:
        rec_container.button("録画停止", on_click=rec_stop)

    stss.method = method_container.radio(
        "処理方法", ["無加工", "二値化", "背景差分"], disabled=bool(stss.rec_status)
    )

    if stss.method == "二値化":
        stss.threshold = slider_container.select_slider(
            "二値化の閾値", options=list(range(256)), value=(90, 180)
        )
    else:
        slider_container.empty()


async def recording_countdown():
    while stss.rec_status == 1:  # ステータスが「開始」の場合
        stss.rec_start = time.time()
        stss.rec_status = 2  # ステータスを「進行中」に更新
    while stss.rec_status == 2:  # ステータスが「進行中」の場合
        passed_time = time.time() - stss.rec_start
        if passed_time >= stss.rec_time:
            stss.rec_status = 3  # ステータスを「終了処理中」に更新
        else:
            await asyncio.sleep(0.1)


async def toast():
    text = "recording."
    count = 0
    while stss.rec_status != 0:
        while stss.rec_status in [1, 2]:
            if count == 0:
                msg = st.toast(text)
            count += 1
            await asyncio.sleep(0.5)
            msg.toast(text + "." * (count % 5))

        while stss.rec_status == 3:  # ステータスが「終了処理中」の場合
            st.toast("recorded!")
            stss.rec_status = 0
            st.rerun()
        while stss.rec_status == 4:  # ステータスが「停止処理中」の場合
            st.toast("recording has been stopped.")
            stss.rec_status = 0
            st.rerun()


async def set_screen():
    if stss.switch == "スクリーン":
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # モニターの情報を取得
            while True:
                img = sct.grab(monitor)  # スクリーンキャプチャを取得
                img = np.array(img)
                img = await add_cursor(img)
                img = await processing(img, stss.method)
                stss.frame = img
                await asyncio.sleep(0.01)


async def set_camera_image():
    while stss.switch == "カメラ":
        ret, img = stss.cap.read()
        if ret:
            stss.frame = await processing(img, stss.method)
        await asyncio.sleep(0.01)


async def processing(img, method):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if method == "二値化":
        img = await bin_partly(img, stss.threshold)
    elif method == "背景差分":
        img = await motion_detection(img, stss.fgbg)
    return img


async def disp_frame(container):
    while True:
        if stss.frame is not None:
            container.image(stss.frame)

        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
