# --coding:utf-8--
import cv2
import numpy as np
import os
import time

def Contrast_andBrightness(alpha, beta, img):
    blank = np.zeros(img.shape, img.dtype)

    dst = cv2.addWeighted(img, alpha, blank, 1-alpha, beta)
    return dst

frame = cv2.imread('/Volumes/SSD/realsense_dataCollection/Group00/20210520_133158/color/00000001_color.png')
frame1 = Contrast_andBrightness(1.5, 100, frame)
frame2 = np.power(frame/float(np.max(frame)), 0.1)
cv2.imshow('frame2', frame2)


key = cv2.waitKey(5000)
if key == 27:
    cv2.destroyAllWindows()

