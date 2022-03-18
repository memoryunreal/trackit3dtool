import cv2
import numpy as np
import os
from multiprocessing import Process
from tkinter import *
from tkinter import filedialog


alpha_slider_max = 100
title_window = 'Linear Blend'

def get_png_filename(input_dir, number):
    dir_path = input_dir
    # color path and colormap path
    color_dir = os.path.join(dir_path, 'color')
    colormap_dir = os.path.join(dir_path, 'colormap')

    # read png file
    color_image = cv2.imread(os.path.join(color_dir, '%08d_color.png' % number))
    colormap_image = cv2.imread(os.path.join(colormap_dir, '%08d_colormap.png' % number))

    return colormap_image, color_image


def on_trackbar(val):
    alpha = val / alpha_slider_max
    beta = (1.0 - alpha)
    dst = cv2.addWeighted(src1, alpha, src2, beta, 0.0)
    merge_dst = np.hstack((dst, src1))
    print("alpha: ", alpha)
    cv2.imshow(title_window, merge_dst)
    

def merge2png(color_image, colormap_image):
    # step_list = [0.02 * x for x in range(0, 51)]

    cv2.namedWindow(title_window)
    trackbar_name = 'Alpha x %d' % alpha_slider_max
    cv2.createTrackbar(trackbar_name, title_window, 0, alpha_slider_max, on_trackbar)

    on_trackbar(0)
    cv2.waitKey(10)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()



if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    dir_name = filedialog.askdirectory()
    input_dir = dir_name
    print(input_dir)
    image_index = 0
    while True:
        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            break
        if pressedKey == ord('a'):
            colormap, color = get_png_filename(input_dir, image_index)
            merge2png(colormap, color)
            
        elif pressedKey == ord('d'):

        
        



