# asyncioを用いて並列処理化
# サクサク動く感じになった
# cv2.VideoCapture(0)を起動時に読み込むようにしたのが大きそう

import asyncio

import cv2
import streamlit as st
from streamlit import session_state as stss


async def main():
    if "frame" not in stss:
        stss.frame = None

    if "switch" not in stss:
        stss.switch = False

    if "binswitch" not in stss:
        stss.binswitch = False

    if "cap" not in stss:
        stss.cap = cv2.VideoCapture(0)

    stss.switch = st.checkbox("カメラ", value=False)
    if not stss.switch:
        return

    stss.binswitch = st.checkbox("マスク処理", value=False)
    # stss.threshold = st.slider("閾値", min_value=0, max_value=255, value=127, step=1)
    stss.threshold = st.select_slider(
        "閾値", options=list(range(256)), value=(100, 150)
    )

    container = st.empty()

    task1 = asyncio.create_task(read_frame())
    task2 = asyncio.create_task(write_frame(container))
    await asyncio.gather(task1, task2)
    stss.cap.release()


async def read_frame():
    while stss.switch:
        ret, img = stss.cap.read()
        if ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if stss.binswitch:
                img = bin_partly(stss.threshold, img)
            stss.frame = img
        await asyncio.sleep(0.001)


def bin_partly(ths, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask1 = cv2.threshold(gray, ths[0], 255, cv2.THRESH_BINARY)
    _, mask2 = cv2.threshold(gray, ths[1], 255, cv2.THRESH_BINARY)
    mask1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2RGB)
    frame = cv2.bitwise_and(frame, mask1)
    frame[mask2 == 255] = [255, 255, 255]
    return frame


async def write_frame(container):
    while stss.switch:
        if stss.frame is not None:
            container.image(stss.frame)
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
