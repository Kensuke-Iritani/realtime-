# asyncioを用いて並列処理化
# サクサク動く感じになった
# グラフを追加した

import asyncio

import cv2
import japanize_matplotlib  # type: ignore
import matplotlib.pyplot as plt
import streamlit as st
from streamlit import session_state as stss


async def main():
    if "frame" not in stss:
        stss.frame = None

    if "switch" not in stss:
        stss.switch = False

    if "cap" not in stss:
        stss.cap = cv2.VideoCapture(0)

    if "hist_fig" not in stss:
        stss.hist_fig, stss.hist_ax = plt.subplots(1, 1, figsize=(10, 4))
        colors = ["b", "g", "r"]
        stss.hist_lines = [stss.hist_ax.plot([], [], color=col)[0] for col in colors]
        stss.hist_ax.set_xlim(0, 256)
        stss.hist_ax.set_ylim(0, 10000)
        stss.hist_ax.set_xlabel("輝度")
        stss.hist_ax.set_ylabel("ピクセル数")
        stss.hist_ax.set_title("Histogram of RGB Channels")
        stss.hist_ax.legend(["Blue", "Green", "Red"])

    stss.switch = st.checkbox("カメラon", value=False)
    container = st.empty()
    hist_container = st.empty()

    if not stss.switch:
        return

    task1 = asyncio.create_task(read_frame())
    task2 = asyncio.create_task(write_frame(container))
    task3 = asyncio.create_task(plot_frame(hist_container))
    await asyncio.gather(task1, task2, task3)
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


async def plot_frame(hist_container):
    while stss.switch:
        if stss.frame is not None:
            update_histogram(stss.frame)
            hist_container.pyplot(stss.hist_fig)
        await asyncio.sleep(1)


def update_histogram(frame):
    color = ("b", "g", "r")
    for i, col in enumerate(color):
        histr = cv2.calcHist([frame], [i], None, [256], [0, 256])
        stss.hist_lines[i].set_data(range(256), histr)
    stss.hist_ax.relim()
    stss.hist_ax.autoscale_view()


if __name__ == "__main__":
    asyncio.run(main())
