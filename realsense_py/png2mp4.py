#####################################################
##               Read bag from file                ##
#####################################################


# First import library
from tkinter import *
import tkinter.filedialog
import time
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import os.path for file path manipulation
import os.path
alpha = 0.6
beta = (1.0 - alpha)

def read_image(dir_list):
    sum_merge_image_list = []

    if os.path.isdir(dir_list):
        color_dir = os.path.join(dir_list, 'color')
        # colormap path
        colormap_dir = os.path.join(dir_list, 'colormap')

        color_image_list = sorted(os.listdir(color_dir))
        colormap_image_list = sorted(os.listdir(colormap_dir))
        color_image_sum = len(color_image_list)
        colormap_image_sum = len(colormap_image_list)
        print(colormap_image_sum, color_image_sum)
        if color_image_sum != colormap_image_sum:
            print("number of color and colormap do not match")

        for i in range(colormap_image_sum):
            color_frames = cv2.imread(os.path.join(color_dir, color_image_list[i]))
            colormap_frames = cv2.imread(os.path.join(colormap_dir, colormap_image_list[i]))
            merge_images = np.hstack((color_frames, colormap_frames))  # display horizontal
            sum_merge_image_list.append(merge_images)
    
    else:
        for dirname in dir_list:
            # color path
            color_dir = os.path.join(dirname, 'color')
            # colormap path
            colormap_dir = os.path.join(dirname, 'colormap')

            color_image_list = sorted(os.listdir(color_dir))
            colormap_image_list = sorted(os.listdir(colormap_dir))
            color_image_sum = len(color_image_list)
            colormap_image_sum = len(colormap_image_list)
            print(colormap_image_sum, color_image_sum)
            if color_image_sum != colormap_image_sum:
                print("number of color and colormap do not match")

            for i in range(colormap_image_sum):
                color_frames = cv2.imread(os.path.join(color_dir, color_image_list[i]))
                colormap_frames = cv2.imread(os.path.join(colormap_dir, colormap_image_list[i]))
                
                dst = cv2.addWeighted(colormap_frames, alpha, color_frames, beta, 0.0)
                merge_images = np.hstack((dst, colormap_frames))  # display horizontal
                sum_merge_image_list.append(merge_images)
    return sum_merge_image_list




def video_write(merge_list, mp4name):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    size = (1280, 480)
    video_writer = cv2.VideoWriter(os.path.join(dir_name, '%s.mp4' % mp4name), fourcc, 10, size)

    color_image_sum = len(merge_list)

    for i in range(color_image_sum):
        try:
            video_writer.write(merge_list[i])
        except RuntimeError as e:
            print('error')


    video_writer.release()


if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    dir_name = tkinter.filedialog.askdirectory(initialdir='/Users/lizhe/Data')
    mp4_name = 'output'

    # sub_dir_namelist = []
    # sub_dir_list = ['backpack01_meetingroom', 'backpack02_meetingroom', 'backpack_lab'
    #     , 'flag_lab', 'human_elevator', 'pikachu_lab', 'paperairplane_lab', 'unfoldingbag_lab']
    # #sub_dir_list = ['chinchilla01_meetingroom']
    # for dirname in sub_dir_list:
    #     sub_dir_namelist.append(os.path.join(dir_name, dirname))
    # merge_image_list = read_image(sub_dir_namelist)
    merge_image_list = read_image(dir_name)
    print(len(merge_image_list))
    video_write(merge_image_list, mp4_name)
