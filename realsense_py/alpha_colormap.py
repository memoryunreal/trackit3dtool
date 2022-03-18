#####################################################
##               Read bag from file                ##
#####################################################


# First import library
from tkinter import *
import tkinter.filedialog
from typing import DefaultDict
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import os.path for file path manipulation
import os.path
import sys


alpha_slider_max = 100
title_window = 'Linear Blend'


def on_trackbar(val):
    alpha1 = (val / alpha_slider_max) * 100
    # beta = (1.0 - alpha)
    # dst = cv2.addWeighted(src1, alpha, src2, beta, 0.0)
    # merge_dst = np.hstack((dst, src1))
    print("alpha: ", alpha1)
    # colormap_JET
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frames, alpha=alpha1), cv2.COLORMAP_JET)
    # colormap_Bone
    # depth_image_map = cv2.convertScaleAbs(depth_frames, alpha=alpha1)
    # depth_colorbone = cv2.applyColorMap(cv2.convertScaleAbs(depth_frames, alpha=alpha1), cv2.COLORMAP_BONE)
    cv2.imshow(title_window, depth_colormap)
    # cv2.imshow(title_window, depth_colorbone) 
    # cv2.imshow(title_window, depth_image_map) 

   


def save_colormap(dir_name):

    color_dir = os.path.join(dir_name, 'color')
    # depth path
    depth_dir = os.path.join(dir_name, 'depth')
    color_image_list = sorted(os.listdir(color_dir))
    depth_image_list = sorted(os.listdir(depth_dir))
    color_image_sum = len(color_image_list)
    depth_image_sum = len(depth_image_list)
    print(depth_image_sum, color_image_sum)
    if color_image_sum != depth_image_sum:
        print("number of color and depth do not match")

    for i in range(1, depth_image_sum+1):
        color_frames = cv2.imread(os.path.join(color_dir, color_image_list[i-1]))
        depth_frames = cv2.imread(os.path.join(depth_dir, depth_image_list[i-1]))
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frames, alpha=8), cv2.COLORMAP_JET)
        # depth_colormap = cv2.applyColorMap(depth_frames, cv2.COLORMAP_JET)
        #merge_images = np.hstack((color_frames, depth_colormap))  # display horizontal
        # cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('Align Example', merge_images )
        cv2.imwrite('%s/%s/%08d_colormap.png'%(dir_name, 'colormap', i), depth_colormap)
        # cv2.imwrite('%s/%s/%08d_depth.png'%(dir_name, 'colormap', i), depth_frames)
        # cv2.imwrite('%s/%s/%08d_colormap.png'%(dir_name, 'colormap', i), merge_images)
         # step_list = [0.02 * x for x in range(0, 51)]
       
    return True



def first_depthframe(dir_name):

    # color_dir = os.path.join(dir_name, 'color')
    # depth path
    depth_dir = os.path.join(dir_name, 'depth')
    # color_image_list = sorted(os.listdir(color_dir))
    depth_image_list = sorted(os.listdir(depth_dir))
    # color_image_sum = len(color_image_list)
    depth_image_sum = len(depth_image_list)
    # print(depth_image_sum, color_image_sum)
    # if color_image_sum != depth_image_sum:
        # print("number of color and depth do not match")

  
    depth_frames = cv2.imread(os.path.join(depth_dir, depth_image_list[50]), cv2.IMREAD_GRAYSCALE)

    return depth_frames


def ini_colormap():

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
    dir_name = tkinter.filedialog.askdirectory(initialdir='/media/silence/DataT')

    # images = save_colormap(dir_name)

    depth_frames = first_depthframe(dir_name)
    ini_colormap()    
  



