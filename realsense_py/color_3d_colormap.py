import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np

from os.path import exists

class plotData():
    stc_dataset_path = '/media/silence/DataT/stc_benchmark/RGBDdataset'
    ptb_dataset_path = '/media/silence/DataT/ptb_benchmark/ptb_workspace'
    depthtrack_dataset_path = '/media/silence/DataT/DepthTrack/test/'
    cdtb_dataset_path = '/media/silence/DataT/CDTB/sequences'
    td_dataset_path = '/media/silence/DataT/dataset_collect2/data_select_02'

    def __init__(self) -> None:
        pass

    def ptb_data(self, filelist: dict):
        filename_save = os.path.join('/home/silence/Pictures/select', 'ptb')
        if not os.path.exists(filename_save):
            os.mkdir(filename_save)
        self.read_color_depth(self.ptb_dataset_path, filelist, filename_save)
    
    def stc_data(self, filelist: dict):
        filename_save = os.path.join('/home/silence/Pictures/select', 'stc')
        if not os.path.exists(filename_save):
            os.mkdir(filename_save)
        self.read_color_depth(self.stc_dataset_path, filelist, filename_save)

    def cdtb_data(self, filelist: dict):
        filename_save = os.path.join('/home/silence/Pictures/select', 'cdtb')
        if not os.path.exists(filename_save):
            os.mkdir(filename_save)
        self.read_color_depth(self.cdtb_dataset_path, filelist, filename_save)
    
    def depthtrack_data(self, filelist: dict):
        filename_save = os.path.join('/home/silence/Pictures/select', 'depthtrack')
        if not os.path.exists(filename_save):
            os.mkdir(filename_save)
        self.read_color_depth(self.depthtrack_dataset_path, filelist, filename_save)

    def td_data(self, filelist: dict):
        filename_save = os.path.join('/home/silence/Pictures/select', '3d_dataset')
        if not os.path.exists(filename_save):
            os.mkdir(filename_save)
        self.read_color_depth(self.depthtrack_dataset_path, filelist, filename_save)
    
    def pair_color_depth(self, colorfilename, depthfilename, rotBox_pts, depth_threshold):

        rgb = colorfilename

        dp = depthfilename

        rgb = cv2.imread(rgb)
        dp = cv2.imread(dp, -1)
        # dirname = os.path.split(seq)[1]
        try:
            dp[dp>depth_threshold] = depth_threshold # ignore some large values,
        except:
            dp = dp
        dp = cv2.normalize(dp, None, 0, 255, cv2.NORM_MINMAX)
        dp = cv2.applyColorMap(np.uint8(dp), cv2.COLORMAP_JET)

        # cv2.putText(rgb, dirname+'  '+colorfilename[-8:], (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)
        
        draw_polygon(rgb, rotBox_pts)
        draw_polygon(dp, rotBox_pts)
        # cv2.imwrite(save_file, rgb)

        # imgs = cv2.hconcat((rgb, dp))
        vconcat_img = cv2.vconcat((rgb, dp))


        return vconcat_img

    def read_color_depth(self, dirpath, dataSelect: dict, dataset: str):
        dir_path = dirpath

    
        cv2.namedWindow(dir_path)

        sequences = dataSelect['dirname']
        frames = dataSelect['frames']
        for i in range(len(sequences)):
            imags = []
            hconcat_img = []
            seq = sequences[i]
            frame_idx_list = frames[i]
            
            for frame_idx in frame_idx_list:
                rotBox_pts = self.read_frame_dir(dirpath, frame_idx, seq)

                ## frame pth
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (seq, 'color', frame_idx))
                if not os.path.exists(colorfilename):
                    colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (seq, 'color', frame_idx))
                depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (seq, 'depth', frame_idx))

                imags.append(self.pair_color_depth(colorfilename, depthfilename, rotBox_pts, depth_threshold))
            hconcat_img = imags[0]
            for i in range(1, len(imags)):
                hconcat_img = cv2.hconcat((hconcat_img,imags[i]))

            while True:
                pressedKey = cv2.waitKey(1) & 0xFF

                if pressedKey == ord('q'):
                    break
                cv2.waitKey(1)   
                cv2.imshow(dir_path, hconcat_img)
                if pressedKey == ord('s'):
                    # file_path = os.path.join(dataset, seq)
                    file_path = dataset

                    if not os.path.exists(file_path):
                        os.mkdir(file_path)
                    save_file = os.path.join(file_path, '%s%s' % (seq, 'select.jpg'))
                    cv2.imwrite(save_file, hconcat_img)
                    break

                    
    def read_frame_dir(self, dirpath, frame_idx, seq):
     
        frame_index = frame_idx
    
        ground_truth_file = os.path.join(dirpath, '%s/%s' % (seq, "groundtruth.txt"))
                
        all_lines = []
        frameline = []
        with open(ground_truth_file, 'r') as f:
            all_lines = f.readlines()
            if frame_index < len(all_lines)+1:
                frameline = all_lines[frame_idx-1][:-1].split(',')
            else:
                raise Exception
            # firstline = frameline[:-1].split(',')        
        if frameline[0] == 'NaN' or frameline[0] == 'nan':
            rectangle = Rectangle(0,0,0,0)
            rotBox_pts = rectangle.get_vertices_points()
            return rotBox_pts
        x,y,w,h= float(frameline[0]), float(frameline[1]), float(frameline[2]), float(frameline[3])
        # read groundtruth and generate four coordinates of rectangle
        rectangle = Rectangle(x, y, w, h)
        rotBox_pts = rectangle.get_vertices_points()

        return rotBox_pts

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class Rectangle:

    def __init__(self, x, y, w, h):
        # Center Point # Height and Width
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        #self.angle = angle  # in radius

    def get_vertices_points(self):
        #x0, y0, width, height, _angle = self.x, self.y, self.w, self.h, self.angle
        # b = math.cos(math.radians(_angle)) * 0.5
        # a = math.sin(math.radians(_angle)) * 0.5
        # xmin, ymin, xmax, ymax = self.xmin, self.ymin, self.xmax, self.ymax
        x, y, w, h = self.x, self.y, self.w, self.h
        xmin = x 
        xmax = x + w
        ymin = y 
        ymax = y + h
        # + = math.cos(_angle) * 0.5dd
        #a = math.sin(_angle) * 0.5
        pt0 = Point(int(xmin), int(ymin))  #### Int !!!!
        pt1 = Point(int(xmax), int(ymin))
        pt2 = Point(int(xmax), int(ymax))
        pt3 = Point(int(xmin), int(ymax))
        pts = [pt0, pt1, pt2, pt3]
        return pts

def draw_polygon(image, pts, colour=(0, 0, 255), thickness=2):
    """
    Draws a rectangle on a given image.
    :param image: What to draw the rectangle on
    :param pts: Array of point objects
    :param colour: Colour of the rectangle edges
    :param thickness: Thickness of the rectangle edges
    :return: Image with a rectangle
    """
    for i in range(0, len(pts)):
        n = (i + 1) if (i + 1) < len(pts) else 0
        cv2.line(image, (pts[i].x, pts[i].y), (pts[n].x, pts[n].y), colour, thickness)

    return image

if __name__ == '__main__':
    depth_threshold = 5000 #default

    ##### ptb threshold #####
    # depth_threshold = 50000
    ##### ptb threshold #####

    ##### depthtrack threshold #####
    # depth_threshold = 3000
    ##### depthtrack threshold #####
    
    ##### cdtb threshold #####
    # depth_threshold = 20000
    ##### cdtb threshold #####

    ##### stc threshold #####
    # depth_threshold = 20000
    ##### stc threshold #####
    
    ptb_select = {'dirname':['new_ex_occ4', 'zcup_move_1', 'bear_front', 'child_no1'], 
    'frames': [[1,25,45], [1,127,254], [1,159,230], [1,44,156]]}

    stc_select = {'dirname':['umbrella_move', 'bag_static', 'funnel_move', 'shoe_move'], 
    'frames': [[1,83,160], [1,140,270], [1,98,190], [1,35,152]]}

    cdtb_select = {'dirname':['box_darkroom_noocc_5', 'backpack_robotarm_lab_occ', 'box_humans_room_occ_1', 'person_outside'], 
    'frames': [[1,468,1741], [1,709,917], [1,783,855], [1, 810, 1728]]}

    depthtrack_select = {'dirname':['backpack_indoor', 'roller_indoor', 'bag01_indoor', 'ball06_indoor'], 
    'frames': [[1,1100,1530], [1,293,810], [1,421,1231], [1, 257, 709]]}
    td_select = {'dirname':['guitar03_2'], 
    'frames': [[1]]}
    
    plot = plotData()
    # plot.stc_data(stc_select)
    # plot.cdtb_data(cdtb_select)
    # plot.depthtrack_data(depthtrack_select)
    # plot.ptb_data(ptb_select)
    plot.td_data(ptb_select)