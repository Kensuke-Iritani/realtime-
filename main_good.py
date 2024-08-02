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

    if "cap" not in stss:
        stss.cap = cv2.VideoCapture(0)

    stss.switch = st.checkbox("カメラon", value=False)
    container = st.empty()

    if not stss.switch:
        return

    task1 = asyncio.create_task(read_frame())
    task2 = asyncio.create_task(write_frame(container))
    await asyncio.gather(task1, task2)
    stss.cap.release()


async def read_frame():
    while stss.switch:
        ret, frame = stss.cap.read()
        if ret:
            stss.frame = frame
        await asyncio.sleep(0.01)


async def write_frame(container):
    while stss.switch:
        if stss.frame is not None:
            container.image(stss.frame, channels="BGR")
        await asyncio.sleep(0.01)


if __name__ == "__main__":
    asyncio.run(main())
