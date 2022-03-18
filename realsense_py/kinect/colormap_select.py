import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np

from os.path import exists



def on_trackbar(val):
    # global alpha1
    global alpha, rgb, dp, title_name
    # alpha1.value = (val / alpha_slider_max) * 100
    alpha = (val / alpha_slider_max) * 20

    dpx = cv2.applyColorMap(cv2.convertScaleAbs(dp, alpha=alpha), cv2.COLORMAP_JET)
    

    # cv2.putText(rgb, dirname+'  '+colorfilename[-8:], (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)


    imgs = cv2.hconcat((rgb, dpx))
    cv2.imshow(title_name, imgs)
    print("on_trckerbar alpha: ", alpha)

def vis_mask(dirPath):
    global alpha, title_name
    sub_dir_list = []
    
    dir_path = dirPath
    dirname_list = os.listdir(dir_path)
    for dirname in dirname_list:
        if os.path.isdir(os.path.join(dir_path, dirname)):
            sub_dir_list.append(os.path.join(dir_path, dirname))
    num_dir = len(sub_dir_list)

    frame_idx = 1
    dir_idx = 0
    # cv2.namedWindow(seq)
    
    cv2.namedWindow(sub_dir_list[dir_idx])

    colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
    if not os.path.exists(colorfilename):
        colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
    depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))


    title_name = sub_dir_list[dir_idx]
    imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename,alpha)
    trackbar_name = 'Alpha x %d' % alpha_slider_max
    cv2.createTrackbar(trackbar_name, sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar)
    
    on_trackbar(20)
    # read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)

    while True:
      
        num_imgs = len(os.listdir(os.path.join(dir_path, '%s/%s' % (sub_dir_list[dir_idx], 'color'))))

        pressedKey = cv2.waitKey(1) & 0xFF

        if pressedKey == ord('q'):
            break
        

        if pressedKey == ord('a'):
            if frame_idx == 1:
                frame_idx = num_imgs
            else:
                frame_idx -= 1

            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))
           
            title_name = sub_dir_list[dir_idx]
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename, alpha)
        elif pressedKey == ord('d'):
            if frame_idx == num_imgs:
                frame_idx = 1
            else:
                frame_idx += 1

            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))

            title_name = sub_dir_list[dir_idx]
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename,alpha)

        # switch sequence
        elif pressedKey == ord('w'):
            if dir_idx == 0 :
                dir_idx = num_dir - 1
                frame_idx = 1
            else:
                dir_idx -= 1
                frame_idx = 1 
 

            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))

            cv2.destroyAllWindows()
            cv2.namedWindow(sub_dir_list[dir_idx])
            title_name = sub_dir_list[dir_idx]
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename,alpha)
            trackbar_name = 'Alpha x %d' % alpha_slider_max
            cv2.createTrackbar(trackbar_name, sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar)
    
            on_trackbar(5*alpha)
        elif pressedKey == ord('s'):
            if dir_idx == num_dir - 1 :
                dir_idx = 0
                frame_idx = 1
            else:
                dir_idx += 1
                frame_idx = 1 

            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))

            cv2.destroyAllWindows()
            cv2.namedWindow(sub_dir_list[dir_idx])
            title_name = sub_dir_list[dir_idx]
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename,alpha)
            trackbar_name = 'Alpha x %d' % alpha_slider_max
            cv2.createTrackbar(trackbar_name, sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar)
    
            on_trackbar(5*alpha)
    cv2.destroyAllWindows()



def read_rgbd_and_draw(seq, colorfilename, depthfilename, alpha):
    global dp,rgb
   
    # rgb = os.path.join(rgb_path, filename)
    rgb = colorfilename
    # filename_dp = filename[:8]+'_depth'
    # filename_dp = dp_path
    dp = depthfilename

    rgb = cv2.imread(rgb)
    dp = cv2.imread(dp, -1)
    dirname = os.path.split(seq)[1]
    print("read_rgbd_and_draw alpha: ", alpha)
    dp = cv2.normalize(dp, None, 0, 255, cv2.NORM_MINMAX)
    dpx = cv2.applyColorMap(cv2.convertScaleAbs(dp, alpha=alpha), cv2.COLORMAP_JET)
    

    cv2.putText(rgb, dirname+'  '+colorfilename[-8:], (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)


    imgs = cv2.hconcat((rgb, dpx))
    cv2.imshow(seq, imgs)


    return imgs



if __name__ == '__main__':


    alpha_slider_max = 100
    alpha = 0
    global dp
    global rgb
    global title_name
    title_name = ''


    stc_dataset_path = '/media/silence/DataT/stc_benchmark/RGBDdataset'

    ptb_dataset_path = '/media/silence/DataT/ptb_benchmark/ptb_workspace'

    depthtrack_dataset_path = '/media/silence/DataT/DepthTrack/test/'
    cdtb_dataset_path = '/media/silence/DataT/CDTB/sequences'

    kinect_dataset_path = '/media/silence/DataT/dataset_collect2/newfiles'
    #vis_mask(rgb_path, dp_path, xml_list, json_list, seq, record_video_flag=False, depth_threshold=args.depth_threshold)
    # vis_mask(ptb_dataset_path)
    # vis_mask(stc_dataset_path)
    # vis_mask(cdtb_dataset_path)
    # vis_mask(depthtrack_dataset_path)
    vis_mask(kinect_dataset_path)

    