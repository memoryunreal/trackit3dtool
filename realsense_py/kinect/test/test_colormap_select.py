import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np
import shutil
from os.path import exists



def on_trackbar_colormap(val):
    # global alpha1
    global colormap_alpha
    # alpha1.value = (val / alpha_slider_max) * 100
    colormap_alpha = (val / alpha_slider_max) * 20
    print("colormap_alpha: ", colormap_alpha)

def on_trackbar_transparent(val):
    global transparent_alpha
    transparent_alpha = val / alpha_slider_max
    print("transparent_alpha: ", transparent_alpha)

    
def on_trackbar_translation_h(val):
    global horizontal_pixnum
    horizontal_pixnum = val -50

def on_trackbar_translation_v(val):
    global vertical_pixnum
    vertical_pixnum = val -50

def vis_mask(dirPath):
    global alpha, title_name, horizontal_pixnum, vertical_pixnum, transparent_alpha
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
    cv2.createTrackbar("colormap_alpha", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_colormap)
    cv2.createTrackbar("transparent_alpha", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_transparent)
    cv2.createTrackbar("vertical pix", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_translation_v)
    cv2.createTrackbar("horizontal pix", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_translation_h)
    
    # horizontal_pixnum = cv2.getTrackbarPos("horizontal pix", sub_dir_list[dir_idx]) - 50
    # vertical_pixnum = cv2.getTrackbarPos("vertical pix", sub_dir_list[dir_idx]) - 50
    horizontal_pixnum = 0
    vertical_pixnum = 0
    imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)
    

    
    # on_trackbar(20)

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
            print("press a; alpha: ", transparent_alpha)
            title_name = sub_dir_list[dir_idx]

            # dp = cv2.imread(depthfilename, -1)
            # if dp.max() > 10000:
            #     print("%s is larger than 10000...: %d" % (depthfilename, dp.max()))
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)
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
            # dp = cv2.imread(depthfilename, -1)
            # print("%s mean value is %f" % (depthfilename, dp.mean()))
            # if dp.max() > 10000:
            #     print("%s is larger than 10000...: %d" % (depthfilename, dp.max()))
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)

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
            cv2.createTrackbar("colormap_alpha", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_colormap)
            cv2.createTrackbar("transparent_alpha", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_transparent)
            cv2.createTrackbar("vertical pix", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_translation_v)
            cv2.createTrackbar("horizontal pix", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_translation_h)

            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)
            # trackbar_name = 'Alpha x %d' % alpha_slider_max
            # cv2.createTrackbar(trackbar_name, sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar)
    
            # on_trackbar(5*alpha)
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
            cv2.createTrackbar("colormap_alpha", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_colormap)
            cv2.createTrackbar("transparent_alpha", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_transparent)
            cv2.createTrackbar("vertical pix", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_translation_v)
            cv2.createTrackbar("horizontal pix", sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar_translation_h)
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)
            # trackbar_name = 'Alpha x %d' % alpha_slider_max
            # cv2.createTrackbar(trackbar_name, sub_dir_list[dir_idx], 0, alpha_slider_max, on_trackbar)
    
            # on_trackbar(5*alpha)
        elif pressedKey == ord('n'):
            # if frame_idx == num_imgs:
            #     frame_idx = 1
            # else:
            #     frame_idx += 1

            # colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            # if not os.path.exists(colorfilename):
            #     colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            # depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))

            # title_name = sub_dir_list[dir_idx]
            # # dp = cv2.imread(depthfilename, -1)
            # # print("%s mean value is %f" % (depthfilename, dp.mean()))
            # # if dp.max() > 10000:
            # #     print("%s is larger than 10000...: %d" % (depthfilename, dp.max()))
            # imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)
            save_new_depth_and_colormap(dir_path, sub_dir_list[dir_idx])
        else: 
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename)

    cv2.destroyAllWindows()



def read_rgbd_and_draw(seq, colorfilename, depthfilename):
    global dp,rgb, horizontal_pixnum, vertical_pixnum, transparent_alpha, colormap_alpha
    print("colormap_alpha: ", colormap_alpha)
    print("transparent_alpha: ", transparent_alpha)
    print("vertical_pixnum: %d pixel" % (vertical_pixnum))
    print("horizontal_pixnum: %d pixel " % (horizontal_pixnum))
    
    
    mat_translation = np.float32([[1,0,horizontal_pixnum],[0,1,vertical_pixnum]])
    # rgb = os.path.join(rgb_path, filename)
    rgb = colorfilename
    # filename_dp = filename[:8]+'_depth'
    # filename_dp = dp_path
    dp = depthfilename

    rgb = cv2.imread(rgb)
    dp = cv2.imread(dp, -1)
    dirname = os.path.split(seq)[1]

    # dp = cv2.normalize(dp, None, 0, 255, cv2.NORM_MINMAX)
    dpx = cv2.warpAffine(dp,mat_translation,(dp.shape[1], dp.shape[0]))
    dpx = cv2.normalize(dpx, None, 0, 255, cv2.NORM_MINMAX)
    # dpx = cv2.applyColorMap(cv2.convertScaleAbs(dp, alpha=colormap_alpha), cv2.COLORMAP_JET)
    colormap = cv2.applyColorMap(cv2.convertScaleAbs(dpx, alpha=colormap_alpha), cv2.COLORMAP_JET)
    

    # cv2.putText(rgb, dirname+'  '+colorfilename[-8:], (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)

    # colormap = cv2.warpAffine(dpx,mat_translation,(dpx.shape[1], dpx.shape[0]))

    dst = cv2.addWeighted(colormap, transparent_alpha, rgb, 1-transparent_alpha, 0.0)
    # merge_dst = np.hstack((dst, orignal_colormap))


    cv2.putText(dst, dirname+'  '+colorfilename[-8:], (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)

    # imgs = cv2.hconcat((dst, dpx))
    imgs = cv2.hconcat((dst, colormap))
    cv2.imshow(seq, imgs)

    return imgs

def save_new_depth_and_colormap(dir_path, sub_dir):
    global dp,rgb, horizontal_pixnum, vertical_pixnum, transparent_alpha, colormap_alpha, save_path
    parameter_colormap = "colormap_alpha: " + str(colormap_alpha) + '\n'
    parameter_transparent = "transparent_alpha: " + str(transparent_alpha) + '\n'
    parameter_vertical = "vertical_pixnum: %d pixel" % (vertical_pixnum) + '\n'
    parameter_horizontal = "horizontal_pixnum: %d pixel " % (horizontal_pixnum) + '\n'

    parameter_comment = ("mat_translation = np.float32([[1,0,horizontal_pixnum],[0,1,vertical_pixnum]]) \n" + 
                        "#[[1,0,20],[0,1,50]]   表示平移变换：其中20表示水平方向上的平移距离，50表示竖直方向上的平移距离。\n" + 
                        "tmp = cv2.normalize(new_depth, None, 0, 255, cv2.NORM_MINMAX) \n" + 
                        "colormap = cv2.applyColorMap(cv2.convertScaleAbs(tmp, alpha=colormap_alpha), cv2.COLORMAP_JET)")
    dirname = os.path.split(sub_dir)[1]
    save_dir_path = os.path.join(save_path, dirname)
    if not os.path.isdir(save_dir_path):
        os.mkdir(save_dir_path)
    save_dp_path = os.path.join(save_dir_path, 'depth')
    if not os.path.isdir(save_dp_path):
        os.mkdir(save_dp_path)
    save_cp_path = os.path.join(save_dir_path, 'colormap')
    if not os.path.isdir(save_cp_path):
        os.mkdir(save_cp_path)
    save_rgb_path = os.path.join(save_dir_path, 'color')
    if not os.path.isdir(save_rgb_path):
        os.mkdir(save_rgb_path)    
    parameter_file = os.path.join(save_dir_path, 'parameter.txt')
    with open(parameter_file, 'w') as f:
        lines = parameter_colormap + parameter_transparent + parameter_vertical + parameter_horizontal + parameter_comment
        f.writelines(lines)

    depth_file_path = os.path.join(dir_path, '%s/%s' % (dirname, 'depth'))
    color_file_path = os.path.join(dir_path, '%s/%s' % (dirname, 'color'))
    all_depth_filename = os.listdir(depth_file_path)
    mat_translation = np.float32([[1,0,horizontal_pixnum],[0,1,vertical_pixnum]])

    for filename_d in all_depth_filename:
        depth_path = os.path.join(depth_file_path, filename_d)
        old_depth = cv2.imread(depth_path, -1)
        new_depth = cv2.warpAffine(old_depth,mat_translation,(old_depth.shape[1], old_depth.shape[0]))
        tmp = cv2.normalize(new_depth, None, 0, 255, cv2.NORM_MINMAX)
        colormap = cv2.applyColorMap(cv2.convertScaleAbs(tmp, alpha=colormap_alpha), cv2.COLORMAP_JET)

        # save path
        save_dp_file = os.path.join(save_dp_path, filename_d)
        save_colormap_file = os.path.join(save_cp_path, filename_d)

        cv2.imwrite(save_dp_file, new_depth)
        cv2.imwrite(save_colormap_file, colormap)
    
    for filename_c in os.listdir(color_file_path):
        rgb_path = os.path.join(color_file_path, filename_c)
      
        save_rgb_file = os.path.join(save_rgb_path, filename_c)
        shutil.copy2(rgb_path, save_rgb_file)


    print("... %s saved！ ..." % dirname)




if __name__ == '__main__':


    alpha_slider_max = 100
    global dp, rgb, title_name, horizontal_pixnum, vertical_pixnum, transparent_alpha, colormap_alpha, save_path
    colormap_alpha = 3
    transparent_alpha = 0
    title_name = ''
    # save_path = '/media/silence/DataT/dataset_collect2/newfiles'
    save_path = '/media/silence/DataT/dataset_collect3/aligned_01'


    # stc_dataset_path = '/media/silence/DataT/stc_benchmark/RGBDdataset'

    # ptb_dataset_path = '/media/silence/DataT/ptb_benchmark/ptb_workspace'

    # depthtrack_dataset_path = '/media/silence/DataT/DepthTrack/test/'
    # cdtb_dataset_path = '/media/silence/DataT/CDTB/sequences'

    kinect_dataset_path = '/media/silence/DataT/yylz_benchmark'
    minghuihongjun_dataset_path = '/media/silence/DataT/dataset_collect2/hongjunminghui'
    hand_dataset_path = '/media/silence/DataT/dataset_collect3/meta_dataset'
    zhidong_path = '/media/silence/DataT/dataset_collect2/redudant/ZhiDong_01/'
    td_select_path = '/media/silence/DataT/outdoor_dataset_collect'
    
    # td_select_path = '/media/silence/DataT/dataset_collect2/outdoor/court_basketball'

    #vis_mask(rgb_path, dp_path, xml_list, json_list, seq, record_video_flag=False, depth_threshold=args.depth_threshold)
    # vis_mask(ptb_dataset_path)
    # vis_mask(stc_dataset_path)
    # vis_mask(cdtb_dataset_path)
    # vis_mask(depthtrack_dataset_path)
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    # vis_mask(kinect_dataset_path)
    # vis_mask(kinect_dataset_path)
    # vis_mask(td_select_path)
    vis_mask(hand_dataset_path)

    