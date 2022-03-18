from PIL import Image, ImageDraw
import json
import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np
import math
import argparse
from os.path import exists

#base_path = "/home/chenhongjun/.vscode-server/programs/rloss-remaster/试标数据/RGBD-test/"
#case = '00000483_color'
#mask_path = base_path+case+".json"

# with open(mask_path, 'r') as f:
#     mask = json.load(f)
# # lineColor = mask['lineColor']
# # fillColor = mask['fillColor']
# shapes = mask['shapes']
# points = shapes[0]['points']

# polypoints = []
# for i, point in enumerate(points):
#     polypoints.append((point[0],point[1]))


# image_path = base_path+case+".png"
# image = Image.open(image_path)

# # mask = Image.new('L', image.size, 255)
# draw = ImageDraw.Draw(image, 'RGBA')
# draw.polygon(polypoints, fill=(128,0,0,128))

# image.save(base_path+case+"_annotated.png")

#################################################################################################################


# def read_xml(xml_file):
#     root = ET.parse(xml_file).getroot()

#     filename = root.find('filename').text

#     bndbox = root.find('object/bndbox')
#     if bndbox:
#         xmin    = float(bndbox.find('xmin').text)
#         ymin    = float(bndbox.find('ymin').text)
#         xmax    = float(bndbox.find('xmax').text)
#         ymax    = float(bndbox.find('ymax').text)
#         #angle = float(robndbox.find('angle').text)

#         return (filename, xmin, ymin, xmax, ymax)
#     else:
#         return (filename, -1, -1, -1, -1)

# def read_json(json_file):
#     #root = ET.parse(xml_file).getroot()

#     #filename = root.find('imagePath').text

#     #mask_flag = root.find('version')
#     #json_file = base_path+case+".json"
#     with open(json_file, 'r') as f:
#         mask = json.load(f)
#     shapes = mask['shapes']
#     points = shapes[0]['points']

#     polypoints = []
#     for i, point in enumerate(points):
#         polypoints.append((point[0],point[1]))
    
#     return polypoints

# class Point:
#     def __init__(self, x, y):
#         self.x = int(x)
#         self.y = int(y)

# class Rectangle:

#     def __init__(self, x, y, w, h):
#         # Center Point # Height and Width
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         #self.angle = angle  # in radius

#     def get_vertices_points(self):
#         #x0, y0, width, height, _angle = self.x, self.y, self.w, self.h, self.angle
#         # b = math.cos(math.radians(_angle)) * 0.5
#         # a = math.sin(math.radians(_angle)) * 0.5
#         # xmin, ymin, xmax, ymax = self.xmin, self.ymin, self.xmax, self.ymax
#         x, y, w, h = self.x, self.y, self.w, self.h
#         xmin = x 
#         xmax = x + w
#         ymin = y 
#         ymax = y + h
#         # + = math.cos(_angle) * 0.5dd
#         #a = math.sin(_angle) * 0.5
#         pt0 = Point(int(xmin), int(ymin))  #### Int !!!!
#         pt1 = Point(int(xmax), int(ymin))
#         pt2 = Point(int(xmax), int(ymax))
#         pt3 = Point(int(xmin), int(ymax))
#         pts = [pt0, pt1, pt2, pt3]
#         return pts

# def draw_polygon(image, pts, colour=(0, 0, 255), thickness=2):
#     """
#     Draws a rectangle on a given image.
#     :param image: What to draw the rectangle on
#     :param pts: Array of point objects
#     :param colour: Colour of the rectangle edges
#     :param thickness: Thickness of the rectangle edges
#     :return: Image with a rectangle
#     """
#     for i in range(0, len(pts)):
#         n = (i + 1) if (i + 1) < len(pts) else 0
#         cv2.line(image, (pts[i].x, pts[i].y), (pts[n].x, pts[n].y), colour, thickness)

#     return image

# def draw_mask(image, polypoints, colour=(255, 0, 255), thickness=2):

#     for i in range(1, len(polypoints)):
#         n = (i+1) if (i+1) < len(polypoints) else 0
#         x0 = int(polypoints[i-1][0])
#         y0 = int(polypoints[i-1][1])
#         x1 = int(polypoints[i][0])
#         y1 = int(polypoints[i][1])
#         cv2.line(image, (x0, y0), (x1, y1), colour, thickness)

#     return image


def vis_mask(dirPath):
    sub_dir_list = []
    polypoints = []
    dir_path = dirPath
    dirname_list = os.listdir(dir_path)
    for dirname in dirname_list:
        if os.path.isdir(os.path.join(dir_path, dirname)):
            sub_dir_list.append(os.path.join(dir_path, dirname))
    num_dir = len(sub_dir_list)
    out = None
    frame_idx = 1
    dir_idx = 0
    # cv2.namedWindow(seq)
    
    cv2.namedWindow(sub_dir_list[dir_idx])


    # rotBox_pts = read_frame_dir(sub_dir_list, frame_idx, dir_idx)


    
    colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
    if not os.path.exists(colorfilename):
        colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
    depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))



    imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename, depth_threshold, out=out)

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
            # filename, rotBox_pts, frame_idx = get_xmlfilename_and_pts(xml_list, frame_idx)
            # rotBox_pts = read_frame_dir(sub_dir_list, frame_idx, dir_idx)

            ## frame pth
            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))

            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename, depth_threshold, out=out)
        elif pressedKey == ord('d'):
            if frame_idx == num_imgs:
                frame_idx = 1
            else:
                frame_idx += 1

            # rotBox_pts = read_frame_dir(sub_dir_list, frame_idx, dir_idx)

            ## frame pth
            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))


            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename, depth_threshold, out=out)
        elif pressedKey == ord('w'):
            if dir_idx == 0 :
                dir_idx = num_dir - 1
                frame_idx = 1
            else:
                dir_idx -= 1
                frame_idx = 1 
 

            # rotBox_pts = read_frame_dir(sub_dir_list, frame_idx, dir_idx)

            ## frame pth
            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))

            cv2.destroyAllWindows()
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename, depth_threshold, out=out)
        
        elif pressedKey == ord('s'):
            if dir_idx == num_dir - 1 :
                dir_idx = 0
                frame_idx = 1
            else:
                dir_idx += 1
                frame_idx = 1 


            # rotBox_pts = read_frame_dir(sub_dir_list, frame_idx, dir_idx)

            ## frame pth
            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (sub_dir_list[dir_idx], 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (sub_dir_list[dir_idx], 'depth', frame_idx))

            cv2.destroyAllWindows()
            imgs = read_rgbd_and_draw(sub_dir_list[dir_idx], colorfilename, depthfilename, depth_threshold, out=out)

    cv2.destroyAllWindows()



def read_rgbd_and_draw(seq, colorfilename, depthfilename, depth_threshold, out=None, alpha=5):

    # rgb = os.path.join(rgb_path, filename)
    rgb = colorfilename
    # filename_dp = filename[:8]+'_depth'
    # filename_dp = dp_path
    dp = depthfilename

    rgb = cv2.imread(rgb)
    dp = cv2.imread(dp, -1)
    dirname = os.path.split(seq)[1]
    try:
        dp[dp>depth_threshold] = depth_threshold # ignore some large values,
    except:
        dp = dp
    dp = cv2.normalize(dp, None, 0, 255, cv2.NORM_MINMAX)
    # dp = cv2.applyColorMap(np.uint8(dp), cv2.COLORMAP_JET)
    dp = cv2.applyColorMap(cv2.convertScaleAbs(dp, alpha=alpha), cv2.COLORMAP_JET)
    

    cv2.putText(rgb, dirname+'  '+colorfilename[-8:], (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255),2)

    # draw_polygon(rgb, rotBox_pts)
    # draw_polygon(dp, rotBox_pts)


    imgs = cv2.hconcat((rgb, dp))

    if out:
        out.write(imgs)

    cv2.imshow(seq, imgs)

    return imgs



# return boundingbox four coordinates
# def read_frame_dir(sub_dir, frame_idx, dir_idx):
#     sub_dir_list = sub_dir
#     frame_index = frame_idx
#     dir_index = dir_idx
#     # ground_truth_file = os.path.join(sub_dir_list[dir_index], "groundtruth.txt")
            
#     all_lines = []
#     firstline = []
#     frameline = []
#     with open(ground_truth_file, 'r') as f:
#         all_lines = f.readlines()
#         if frame_index < len(all_lines)+1:
#             frameline = all_lines[frame_idx-1][:-1].split(',')
#         else:
#             raise Exception
#         # firstline = frameline[:-1].split(',')        
#     if frameline[0] == 'NaN' or frameline[0] == 'nan':
#         rectangle = Rectangle(0,0,0,0)
#         rotBox_pts = rectangle.get_vertices_points()
#         return rotBox_pts
#     x,y,w,h= float(frameline[0]), float(frameline[1]), float(frameline[2]), float(frameline[3])
#     # read groundtruth and generate four coordinates of rectangle
#     rectangle = Rectangle(x, y, w, h)
#     rotBox_pts = rectangle.get_vertices_points()

#     return rotBox_pts


class plotData():
    stc_dataset_path = '/media/silence/DataT/stc_benchmark/RGBDdataset'
    ptb_dataset_path = '/media/silence/DataT/ptb_benchmark/ptb_workspace'
    depthtrack_dataset_path = '/media/silence/DataT/DepthTrack/test/'
    cdtb_dataset_path = '/media/silence/DataT/CDTB/sequences'

    def __init__(self) -> None:
        pass

    def ptb_data(self, filelist: dict):
        self.read_color_depth(ptb_dataset_path, filelist)
        
    
    def pair_color_depth(self, colorfilename, depthfilename, depth_threshold):

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

        # draw_polygon(rgb, rotBox_pts)
        # draw_polygon(dp, rotBox_pts)

        # imgs = cv2.hconcat((rgb, dp))
        vconcat_img = cv2.vconcat((rgb, dp))


        # cv2.imshow(seq, imgs)

        return vconcat_img

    def read_color_depth(self, dirpath, dataSelect: dict):
        sub_dir_list = []
        dir_path = dirpath
        data_select = dataSelect
        imags = []
        hconcat_img = []
        cv2.namedWindow(dirpath)

        for seq, frame_idx in data_select:

            # rotBox_pts = self.read_frame_dir(dirpath, frame_idx, seq)

            ## frame pth
            colorfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (seq, 'color', frame_idx))
            if not os.path.exists(colorfilename):
                colorfilename = os.path.join(dir_path, '%s/%s/%08d.jpg' % (seq, 'color', frame_idx))
            depthfilename = os.path.join(dir_path, '%s/%s/%08d.png' % (seq, 'depth', frame_idx))

            imags.append(self.pair_color_depth(colorfilename, depthfilename, depth_threshold))
        for img in imags:
            hconcat_img = cv2.hconcat((hconcat_img, img))
        
        cv2.imshow(dirpath, hconcat_img)

    # def read_frame_dir(self, dirpath, frame_idx, seq):
     
    #     frame_index = frame_idx
    
    #     # ground_truth_file = os.path.join(dirpath, '%s/%s' % (seq, "groundtruth.txt"))
                
    #     all_lines = []
    #     frameline = []
    #     # with open(ground_truth_file, 'r') as f:
    #     #     all_lines = f.readlines()
    #     #     if frame_index < len(all_lines)+1:
    #     #         frameline = all_lines[frame_idx-1][:-1].split(',')
    #     #     else:
    #     #         raise Exception
    #         # firstline = frameline[:-1].split(',')        
    #     if frameline[0] == 'NaN' or frameline[0] == 'nan':
    #         rectangle = Rectangle(0,0,0,0)
    #         rotBox_pts = rectangle.get_vertices_points()
    #         return rotBox_pts
    #     x,y,w,h= float(frameline[0]), float(frameline[1]), float(frameline[2]), float(frameline[3])
    #     # read groundtruth and generate four coordinates of rectangle
    #     rectangle = Rectangle(x, y, w, h)
    #     rotBox_pts = rectangle.get_vertices_points()

    #     return rotBox_pts

if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('seq', type=str, default='adapter01_indoor')
    # parser.add_argument('depth_threshold', type=float, default=5000)

    # args = parser.parse_args()

    depth_threshold = 50000 #default


    ##### depthtrack threshold #####
    # depth_threshold = 3000
    ##### depthtrack threshold #####
    
    ##### cdtb threshold #####
    # depth_threshold = 20000
    ##### cdtb threshold #####

    ##### stc threshold #####
    # depth_threshold = 20000
    ##### stc threshold #####

    stc_dataset_path = '/media/silence/DataT/stc_benchmark/RGBDdataset'

    ptb_dataset_path = '/media/silence/DataT/ptb_benchmark/ptb_workspace'

    depthtrack_dataset_path = '/media/silence/DataT/DepthTrack/test/'
    cdtb_dataset_path = '/media/silence/DataT/CDTB/sequences'

    kinect_dataset_path = '/media/silence/DataT/dataset_collect2/yjy'
    #vis_mask(rgb_path, dp_path, xml_list, json_list, seq, record_video_flag=False, depth_threshold=args.depth_threshold)
    # vis_mask(ptb_dataset_path)
    # vis_mask(stc_dataset_path)
    # vis_mask(cdtb_dataset_path)
    # vis_mask(depthtrack_dataset_path)
    vis_mask(kinect_dataset_path)

    