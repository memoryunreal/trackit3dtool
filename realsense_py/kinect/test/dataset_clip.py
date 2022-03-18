import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from shutil import copy2, copyfile, copytree
from os.path import exists

class clipData():


    def __init__(self) -> None:
        
        pass

    def kinect_data(self, filelist: dict):
        self.select_path = os.path.join(dataset_dir)
        # if not os.path.exists(self.select_save):
            # os.mkdir(self.select_save)
        
        # self.clip_color_depth(filelist)
        # self.rename_color_depth(filelist)
        self.copy_clip_color_depth(filelist)

    def clip_color_depth(self, dataSelect: dict):

        dir_path = self.select_path
        log_file = os.path.join(dir_path, 'cliplog.txt')
        
        sequences = dataSelect['dirname']
        frames = dataSelect['frames']
        for i in range(len(sequences)):
            f_log = open(log_file, 'a')
            seq = sequences[i]
            frame_start = int(frames[i][0])
            frame_end = int(frames[i][1])

            color_path = os.path.join(dir_path, '%s/%s' % (seq, 'color'))
            depth_path = os.path.join(dir_path, '%s/%s' % (seq, 'depth'))
            colormap_path = os.path.join(dir_path, '%s/%s' % (seq, 'colormap'))

           
                

            # read color frames name
            color_frames = os.listdir(color_path)
            color_index_list = []
            for colorfile in color_frames:
                color_index = colorfile.split('.')[0]
                color_index_list.append(color_index)
            # sort frames 
            color_index_list.sort()



            for name in color_index_list:
                ## frame path
                
                colorfile_name = os.path.join(color_path, '%s.jpg' % name)
                if not os.path.exists(colorfile_name):
                    colorfile_name = os.path.join(color_path, '%s.png' % name)

                depthfile_name = os.path.join(depth_path, '%s.png' % name)
                colormapfile_name = os.path.join(colormap_path, '%s.png' % name)
                
                # remove no select data
                if int(name) not in range(frame_start, frame_end+1):
                    os.remove(colorfile_name)
                    os.remove(depthfile_name)
                    os.remove(colormapfile_name)
                    print("%s \t --> \t %s" % (colorfile_name, 'remove'), file= f_log)
                    print("%s \t --> \t %s" % (depthfile_name, 'remove'), file=f_log)
                    print("%s \t --> \t %s" % (colormapfile_name, 'remove'), file=f_log)
                    continue
                
                # f_log.close()
                # imags.append(self.pair_color_depth(colorfilename, depthfilename, rotBox_pts, depth_threshold))
            f_log.close()

    def copy_clip_color_depth(self, dataSelect: dict):

        dir_path = self.select_path
        log_file = os.path.join(save_new_file, 'copylog.txt')
        
        sequences = dataSelect['dirname']
        frames = dataSelect['frames']
        for i in range(len(sequences)):
            # new suffix name of sequence
            new_dir_suffix = 1

            for frame in frames[i]:

       
                new_frame_indx = 1
                f_log = open(log_file, 'a')
                seq = sequences[i]

                # list number
                if isinstance(frame, int):
                    new_seq = seq
                    if frame == frames[i][1]:
                        break
                    frame = frames[i]
                else:
                    # new copy path
                    new_seq = seq + '_%d' % new_dir_suffix

                frame_start = int(frame[0])
                frame_end = int(frame[1])

                # original data path
                color_path = os.path.join(dir_path, '%s/%s' % (seq, 'color'))
                depth_path = os.path.join(dir_path, '%s/%s' % (seq, 'depth'))
                colormap_path = os.path.join(dir_path, '%s/%s' % (seq, 'colormap'))




                cp_color_path = os.path.join(save_new_file, '%s/%s' % (new_seq, 'color'))
                cp_depth_path = os.path.join(save_new_file, '%s/%s' % (new_seq, 'depth'))
                cp_colormap_path = os.path.join(save_new_file, '%s/%s' % (new_seq, 'colormap')) 

                if not os.path.exists(os.path.join(save_new_file, new_seq)):
                    # create dir
                    os.mkdir(os.path.join(save_new_file, new_seq))
                    os.mkdir(cp_color_path)
                    os.mkdir(cp_depth_path)
                    os.mkdir(cp_colormap_path)       
                    

                # read color frames name
                color_frames = os.listdir(color_path)
                color_index_list = []
                for colorfile in color_frames:
                    color_index = colorfile.split('.')[0]
                    color_index_list.append(color_index)
                # sort frames 
                color_index_list.sort()



                for name in color_index_list:
                    ## frame path
                    bool_jpg = 0
                    colorfile_name = os.path.join(color_path, '%s.jpg' % name)
                    if not os.path.exists(colorfile_name):
                        bool_jpg = 1
                        colorfile_name = os.path.join(color_path, '%s.png' % name)

                    depthfile_name = os.path.join(depth_path, '%s.png' % name)
                    colormapfile_name = os.path.join(colormap_path, '%s.png' % name)
                    # copy selected data to other path
                    if int(name) not in range(frame_start, frame_end+1):

                        print("%s \t --> \t %s" % (colorfile_name, "not selected"), file= f_log)
                        print("%s \t --> \t %s" % (depthfile_name, "not selected"), file=f_log)
                        print("%s \t --> \t %s" % (colormapfile_name, "not selected"), file=f_log)
                        continue
                    else: 

                        
                        # define copy file destinate path
                        cp_colorfile_name = os.path.join(cp_color_path, '%08d.jpg' % new_frame_indx)
                        # if not os.path.exists(colorfile_name):
                        if bool_jpg:
                            cp_colorfile_name = os.path.join(cp_color_path, '%008d.png' % new_frame_indx)

                        cp_depthfile_name = os.path.join(cp_depth_path, '%08d.png' % new_frame_indx)
                        cp_colormapfile_name = os.path.join(cp_colormap_path, '%08d.png' % new_frame_indx)
                        copy2(colorfile_name, cp_colorfile_name )
                        copy2(depthfile_name, cp_depthfile_name)
                        copy2(colormapfile_name, cp_colormapfile_name)
                        new_frame_indx += 1

                        print("%s \t --> \t %s" % (colorfile_name, cp_colorfile_name), file= f_log)
                        print("%s \t --> \t %s" % (depthfile_name, cp_depthfile_name), file=f_log)
                        print("%s \t --> \t %s" % (colormapfile_name, cp_colormapfile_name), file=f_log)               
                
                # suffix + 1
                new_dir_suffix += 1
                f_log.close()


    def rename_color_depth(self, dataSelect: dict):
        
        dir_path = self.select_save
        log_file = os.path.join(dir_path, 'renamelog.txt')
        
        sequences = dataSelect['dirname']
        frames = dataSelect['frames']
        for i in range(len(sequences)):
            f_log = open(log_file, 'a')
            seq = sequences[i]
            color_path = os.path.join(dir_path, '%s/%s' % (seq, 'color'))
            depth_path = os.path.join(dir_path, '%s/%s' % (seq, 'depth'))
            colormap_path = os.path.join(dir_path, '%s/%s' % (seq, 'colormap'))

           
                

            # read color frames name
            color_frames = os.listdir(color_path)
            color_index_list = []
            for colorfile in color_frames:
                color_index = colorfile.split('.')[0]
                color_index_list.append(color_index)
            # sort frames 
            color_index_list.sort()



            for name in color_index_list:
                ## frame path
                
                colorfile_name = os.path.join(color_path, '%s.jpg' % name)
                if not os.path.exists(colorfile_name):
                    colorfile_name = os.path.join(color_path, '%s.png' % name)

                depthfile_name = os.path.join(depth_path, '%s.png' % name)
                colormapfile_name = os.path.join(colormap_path, '%s.png' % name)
                
                # f_log.close()
                # generate new index
                new_name = color_index_list.index(name) + 1

                
                new_color_name = os.path.join(color_path, '%08d.jpg' % new_name)
                new_depth_name = os.path.join(depth_path, '%08d.png' % new_name)
                new_colormap_name = os.path.join(colormap_path, '%08d.png' % new_name)
                os.rename(colorfile_name, new_color_name)
                os.rename(depthfile_name, new_depth_name)
                os.rename(colormapfile_name, new_colormap_name)
                
                print("%s \t --> \t %s" % (colorfile_name, new_color_name), file= f_log)
                print("%s \t --> \t %s" % (depthfile_name, new_depth_name), file=f_log)
                print("%s \t --> \t %s" % (colormapfile_name, new_colormap_name), file=f_log)

                # f_log.close()
                # imags.append(self.pair_color_depth(colorfilename, depthfilename, rotBox_pts, depth_threshold))
            f_log.close()


  

if __name__ == '__main__':

    #kinect_select = {'dirname': ['backpack07', 'backpack04', 'balloon01', 'balloon02', 'balloon03',
    #                             'basketball02', 'box03', 'box05', 'box07', 'box08', 'bucket01', 'chair01',
    #                             'displayer02', 'earth01', 'fire_extinguisher01', 'guitar01', 'guitar03'],
    #                 'frames': [[[20, 120], [172, 295]], [[64, 144], [170, 290], [560, 660]], [[31, 106], [362, 524]], [[168, 268], [497, 541]], [[19, 82], [130, 353]],
    #                           [[22, 70], [217, 328], [456, 556]], [[22, 223], [274, 360]], [1, 170], [[35, 140], [141, 357]], [
    #                                [64, 218], [235, 370], [371, 549]], [[160, 290], [291, 390], [391, 531], [755, 910]], [[18, 125], [128, 342]],
    #                            [[1, 126], [200, 335]], [[20, 104], [340, 440], [480, 606]], [[16, 126], [168, 294]], [[350, 450], [520, 636]], [[40, 200], [280, 380]]]}

    kinect_select = {'dirname':['badmintonplayer', 'basketballplayer', 'bike', 'child01', 'dinasor01', 'dinasor02',
                    'gas', 'gym_dancer', 'horse01', 'human_shoppingmall', 'pottedplant', 'redball',
                    'robotics_arm01', 'robotics_arm02', 'trashbin', 'woodblock', 'yellowball', 'yogaball'], 
    'frames': [[282,400], [50,178], [1,172], [1,166], [[1,180],[220,420]],[300,490], 
                [[50,250],[250,460],[461,713]], [[1,248],[248,448]], [[1,105],[60,180],[130,300]], [[1,170],[277,356]], [1,184], [1,205],
                [[190,340],[355,495]], [[700,900], [900,1100]],[[1,90],[282,435]], [100,282], [1,138], [1,263] ]}
    kinect_select01 = {'dirname':['kettlebell'], 
    'frames': [[222,400]]}

    hand_select03 =  {'dirname':['bull', 'cube01', 'cube02', 'milkbox', 'pen', 'tissuebox',
                    'toy_car01', 'turtlebox01', 'turtlebox02', 'watercup', 'laptop01', 'laptop02',
                    'book02', 'head01', 'hand_gesture01'], 
    'frames': [[1, 365], [1, 162], [62, 600], [7, 220], [1, 555], [1, 747], 
                [1, 600], [555, 1000], [403, 582], [15, 590], [229, 353], [1, 146],
                [574, 715], [179, 280], [[31, 142], [440, 650], [770, 959]]]}
    hand_select03_1 =  {'dirname':['hand_gesture01'], 
    'frames': [ [[31, 142], [440, 650], [770, 959]]]}
    dataset_dir = '/media/silence/DataT/dataset_collect3/aligned_01'
    save_new_file = '/media/silence/DataT/dataset_collect3/clipped_02'
    # plot = clipData()

    # plot.kinect_data(kinect_select)
    copy_clip = clipData()
    copy_clip.kinect_data(hand_select03)
