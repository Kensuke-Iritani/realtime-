import cv2
import numpy as np
import pyautogui
from PIL import Image

cursor_image_path = "cursor.png"


async def add_cursor(img):
    img = Image.fromarray(img)
    cursor_x, cursor_y = pyautogui.position()  # マウスカーソルの位置を取得
    cursor_img = Image.open(cursor_image_path)
    img.paste(cursor_img, (cursor_x, cursor_y), cursor_img)
    return np.array(img)


async def bin_partly(img, ths):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask1 = cv2.threshold(gray, ths[0], 255, cv2.THRESH_BINARY)
    _, mask2 = cv2.threshold(gray, ths[1], 255, cv2.THRESH_BINARY)
    mask1 = cv2.cvtColor(mask1, cv2.COLOR_GRAY2RGB)
    img = cv2.bitwise_and(img, mask1)
    img[mask2 == 255] = [255, 255, 255]
    return img


async def motion_detection(img, fgbg):
    fgmask = fgbg.apply(img)
    # print(np.sum(fgmask.astype(np.uint64)) / 255 / fgmask.shape[0] / fgmask.shape[1])
    fgmask = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2RGB)
    img = cv2.bitwise_and(img, fgmask)
    return img
