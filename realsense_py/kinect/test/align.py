import cv2
import numpy as np
import os
from tkinter import *
from tkinter import filedialog

alpha_slider_max = 100
title_window = 'Linear Blend'

def get_png_filename(input_dir):
    dir_path = input_dir
    # color path and colormap path
    color_dir = os.path.join(dir_path, 'color')
    depth_dir = os.path.join(dir_path, 'depth')

    # read png file
    color_image = cv2.imread(os.path.join(color_dir, '%08d.jpg' % 50))
    depth_image = cv2.imread(os.path.join(depth_dir, '%08d.png' % 50))
    colormap_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=4), cv2.COLORMAP_JET)

    # colormap_image = cv2.imread(os.path.join(colormap_dir, '%08d.png' % 1))

    return colormap_image, color_image


# def on_trackbar_vertical(val):
#     global dst
#     vertical_pixnum = int(val)-50
#     vertical_translation=np.float32([[1,0,0],[0,1,vertical_pixnum]])  #变换矩阵：设置平移变换所需的计算矩阵：2行3列
#     #[[1,0,20],[0,1,50]]   表示平移变换：其中20表示水平方向上的平移距离，50表示竖直方向上的平移距离。
#     # vertical tranlation
#     dst=cv2.warpAffine(src1, vertical_translation,(960,540))
#     merge_dst = np.hstack((dst, src1))
#     print("vertical transport pixel number: ", vertical_pixnum)
#     cv2.imshow(title_window, merge_dst)

# def on_trackbar_transparent(val):
#     global colormap
#     alpha = val / alpha_slider_max
#     beta = (1.0 - alpha)
#     colormap = 
#     colormap = cv2.addWeighted(colormap, alpha, color, beta, 0.0)

#     merge_dst = np.hstack((dst, orignal_colormap))
#     print("alpha: ", alpha)
#     cv2.imshow(title_window, merge_dst)

def on_trackbar_transparent(val):
    global alpha
    alpha = val / alpha_slider_max
    print("alpha: ", alpha)

    
def on_trackbar_translation(val):

    pass


def merge2png():
    # step_list = [0.02 * x for x in range(0, 51)]
    global horizontal_pixnum, vertical_pixnum, alpha
    while True:
        horizontal_pixnum = cv2.getTrackbarPos("horizontal pix", title_window) - 50
        vertical_pixnum = cv2.getTrackbarPos("vertical pix", title_window) - 50
        mat_translation = np.float32([[1,0,horizontal_pixnum],[0,1,vertical_pixnum]])
        colormap = cv2.warpAffine(orignal_colormap,mat_translation,(960,540))
        dst = cv2.addWeighted(colormap, alpha, color, 1-alpha, 0.0)
        merge_dst = np.hstack((dst, orignal_colormap))
        cv2.imshow(title_window, merge_dst)
     

        if cv2.waitKey(10) == 27:
            cv2.destroyAllWindows()



if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    dir_name = filedialog.askdirectory(initialdir='/media/silence/DataT/dataset_collect2/ZhiDong_01/book-01')
    input_dir = dir_name
    print(input_dir)
    global horizontal_pixnum, vertical_pixnum, alpha
    alpha = 0
    orignal_colormap, color = get_png_filename(input_dir)
    # orignal_colormap = colormap
    # mat_translation=np.float32([[1,0,0],[0,1,7]])  #变换矩阵：设置平移变换所需的计算矩阵：2行3列
    #[[1,0,20],[0,1,50]]   表示平移变换：其中20表示水平方向上的平移距离，50表示竖直方向上的平移距离。
    # src1=cv2.warpAffine(src1,mat_translation,(960,540))  #变换函数
    '''
    参数2 变换矩阵：是一个2行3列的矩阵，由这个矩阵决定是何种变换
    参数3 变换后输出图像的大小:(width+20,height+50)-->宽和高(自己规定)
    参数4 可选参数，用于设置插值方法的组合，默认为INTER_LINEAR使用线性插值算法，除了图像缩放中用到的几个插值算法外，仿射变换还可以选用
    INTER_LANCZOS4（Lanczos插值算法）。
    参数5 borderValue：可选参数，在边界不变的情况下可以使用的值，主要用于设置边界的填充值，默认为0
    '''
    cv2.namedWindow(title_window)
    trackbar_name = 'Alpha x %d' % alpha_slider_max
    cv2.createTrackbar("transparent_alpha", title_window, 0, alpha_slider_max, on_trackbar_transparent)
    cv2.createTrackbar("vertical pix", title_window, 0, alpha_slider_max, on_trackbar_translation )
    cv2.createTrackbar("horizontal pix", title_window, 0, alpha_slider_max, on_trackbar_translation)
    on_trackbar_translation(50)
    merge2png()
