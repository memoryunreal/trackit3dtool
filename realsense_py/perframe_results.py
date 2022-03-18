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

def read_rgbd_and_draw(rgb_path, dp_path, seq, filename, rotBox_pts, polypoints, depth_threshold, out=None):

    rgb = os.path.join(rgb_path, filename)
    filename_dp = filename[:8]+''
    dp = os.path.join(dp_path, filename_dp+'.png')

    rgb = cv2.imread(rgb)
    dp = cv2.imread(dp, -1)

    try:
        dp[dp>depth_threshold] = depth_threshold # ignore some large values,
    except:
        dp = dp
    dp = cv2.normalize(dp, None, 0, 255, cv2.NORM_MINMAX)
    dp = cv2.applyColorMap(np.uint8(dp), cv2.COLORMAP_JET)

    cv2.putText(rgb,filename, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 255, 255),2)

    draw_polygon(rgb, rotBox_pts)
    draw_polygon(dp, rotBox_pts)
    #draw = ImageDraw.Draw(rgb)
    #draw = ImageDraw.Draw(dp)
    #rgb.polygon(polypoints, fill=(128,0,0,128))
    #dp.polygon(polypoints, fill=(128,0,0,128))
    draw_mask(rgb, polypoints)
    draw_mask(dp, polypoints)
    # cv2.imwrite("/home/silence/3d.jpg", rgb)
    imgs = cv2.hconcat((rgb, dp))

    if out:
        out.write(imgs)

    cv2.imshow(seq, imgs)

    return imgs

def read_xml(xml_file):
    root = ET.parse(xml_file).getroot()

    filename = root.find('filename').text

    bndbox = root.find('object/bndbox')
    if bndbox:
        xmin    = float(bndbox.find('xmin').text)
        ymin    = float(bndbox.find('ymin').text)
        xmax    = float(bndbox.find('xmax').text)
        ymax    = float(bndbox.find('ymax').text)
        #angle = float(robndbox.find('angle').text)

        return (filename, xmin, ymin, xmax, ymax)
    else:
        return (filename, -1, -1, -1, -1)

def read_json(json_file):
    #root = ET.parse(xml_file).getroot()

    #filename = root.find('imagePath').text

    #mask_flag = root.find('version')
    #json_file = base_path+case+".json"
    with open(json_file, 'r') as f:
        mask = json.load(f)
    shapes = mask['shapes']
    points = shapes[0]['points']

    polypoints = []
    for i, point in enumerate(points):
        polypoints.append((point[0],point[1]))
    
    return polypoints

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class Rectangle:

    def __init__(self, xmin, ymin, xmax, ymax):
        # Center Point # Height and Width
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        #self.angle = angle  # in radius

    def get_vertices_points(self):
        #x0, y0, width, height, _angle = self.x, self.y, self.w, self.h, self.angle
        # b = math.cos(math.radians(_angle)) * 0.5
        # a = math.sin(math.radians(_angle)) * 0.5
        xmin, ymin, xmax, ymax = self.xmin, self.ymin, self.xmax, self.ymax
        #b = math.cos(_angle) * 0.5
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

def draw_mask(image, polypoints, colour=(255, 0, 255), thickness=2):

    for i in range(1, len(polypoints)):
        n = (i+1) if (i+1) < len(polypoints) else 0
        x0 = int(polypoints[i-1][0])
        y0 = int(polypoints[i-1][1])
        x1 = int(polypoints[i][0])
        y1 = int(polypoints[i][1])
        cv2.line(image, (x0, y0), (x1, y1), colour, thickness)

    return image

def write_rotated2file(all_pts, out_file):
    with open(out_file, 'w') as fp:
        for pts in all_pts :
            if pts[0].x > -1 and pts[0].y > -1 and pts[1].x > -1 and pts[1].y > -1:
                fp.write('%f,%f,%f,%f,%f,%f,%f,%f\n'%(pts[0].x, pts[0].y, pts[1].x, pts[1].y, pts[2].x, pts[2].y, pts[3].x, pts[3].y))
            else:
                fp.write('Nan,Nan,Nan,Nan,Nan,Nan,Nan,Nan\n')

def get_xmlfilename_and_pts(xml_list, frame_idx):
    #
    #xml_file = os.path.join(base_path, xml)
    xml_file = os.path.join(base_path, '%08d.xml'%frame_idx)
    if os.path.exists(xml_file):
        (filename, xmin, ymin, xmax, ymax) = read_xml(xml_file)
    else: 
        xml = xml_list[frame_idx]
        frame_idx = int(xml[:8])
        filename, rotBox_pts,frame_idx = get_xmlfilename_and_pts(xml_list, frame_idx)
        xml_file = os.path.join(base_path, '%08d_color.xml'%frame_idx)
        (filename, xmin, ymin, xmax, ymax) = read_xml(xml_file)
    #print(filename, xmin, ymin, xmax, ymax)

    rectangle = Rectangle(xmin, ymin, xmax, ymax)
    rotBox_pts = rectangle.get_vertices_points()

    return filename, rotBox_pts,frame_idx

def get_jsonfilename_and_pts(json_list, frame_idx):
    #json = json_list[frame_idx]
    json_file = os.path.join(base_path, '%08d.json'%frame_idx)
    #json_file = os.path.join(base_path, json)
    polypoints = read_json(json_file)
    print(json_file)
    #print(filename, polypoints)

    #rectangle = Rectangle(cx, cy, w, h, angle)
    #rotBox_pts = rectangle.get_vertices_points()

    return polypoints

def vis_mask(rgb_path, dp_path, xml_list, json_list, seq,
                                 record_video_flag=False, depth_threshold=8000):

    num_imgs = len(xml_list)

    if record_video_flag:
        framerate  = 30
        windowsize = (1280, 360)
        out = cv2.VideoWriter('%s.avi'%seq, cv2.VideoWriter_fourcc('M','J','P','G'), framerate, windowsize)
    else:
        out = None

    cv2.namedWindow(seq)

    frame_idx = int(xml_list[0][:8])
    result_idx = frame_idx
    filename, rotBox_pts, frame_idx = get_xmlfilename_and_pts(xml_list, frame_idx)
    # json_file = os.path.join(base_path, '00000000.json')
    # if json_file:
    #     polypoints = get_jsonfilename_and_pts(json_list, frame_idx)
    # else:
    #     polypoints = []
    polypoints = get_jsonfilename_and_pts(json_list, frame_idx)
    imgs = read_rgbd_and_draw(rgb_path, dp_path, seq, filename, rotBox_pts, polypoints, depth_threshold, out=out)

    while True:
        pressedKey = cv2.waitKey(1) & 0xFF

        if pressedKey == ord('q'):
            break

        if record_video_flag:
            # If record, just one loop
            if frame_idx < num_imgs-1:
                frame_idx += 10
                #frame_idx = int(filename[:8])
                filename, rotBox_pts, frame_idx = get_xmlfilename_and_pts(xml_list, frame_idx)
                json_file = os.path.join(base_path, '%08d.json'%frame_idx)
                if exists(json_file):
                    polypoints = get_jsonfilename_and_pts(json_list, frame_idx)
                else:
                    polypoints = []
                imgs = read_rgbd_and_draw(rgb_path, dp_path, seq, filename, rotBox_pts, polypoints, depth_threshold, out=out)
            else:
                break
        else:
            if pressedKey == ord('a'):
                if frame_idx == 0:
                    frame_idx = num_imgs -1
                else:
                    frame_idx -= 10
                filename, rotBox_pts, frame_idx = get_xmlfilename_and_pts(xml_list, frame_idx)
                json_file = os.path.join(base_path, '%08d.json'%frame_idx)
                if exists(json_file):
                    polypoints = get_jsonfilename_and_pts(json_list, frame_idx)
                else:
                    polypoints = []
                imgs = read_rgbd_and_draw(rgb_path, dp_path, seq, filename, rotBox_pts, polypoints, depth_threshold, out=out)
            elif pressedKey == ord('d'):
                if frame_idx == num_imgs - 1:
                    frame_idx = 0
                else:
                    frame_idx += 10
                filename, rotBox_pts, frame_idx = get_xmlfilename_and_pts(xml_list, frame_idx)
                json_file = os.path.join(base_path, '%08d.json'%frame_idx)
                #json_file = os.path.exists(base_path + frame_idx + '_color.json')
                if exists(json_file):
                    polypoints = get_jsonfilename_and_pts(json_list, frame_idx)
                else:
                    polypoints = []
                imgs = read_rgbd_and_draw(rgb_path, dp_path, seq, filename, rotBox_pts, polypoints, depth_threshold, out=out)

    cv2.destroyAllWindows()

    if record_video_flag:
        out.release()

    # write_rotated2file(all_pts, out_file)





if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('seq', type=str, default='adapter01_indoor')
    # parser.add_argument('depth_threshold', type=float, default=5000)

    # args = parser.parse_args()

    # seq = args.seq
    # #xml_path = '/home/yjy/Downloads/part2_1/%s/color/'%seq
    # #rgb_path = '/home/yjy/Downloads/part2_1/%s/color/'%seq
    # #dp_path  = '/home/yjy/workspace/sequences/%s/depth/'%seq
    seq = 'guitar03'
    depth_threshold = 5000
    base_path = '/media/silence/DataT/dataset_collect2/data_select_100/%s/'%seq
    rgb_path = '/media/silence/DataT/dataset_collect2/data_select_100/%s/color'%seq
    dp_path = '/media/silence/DataT/dataset_collect2/data_select_100/%s/depth'%seq

    base_list = os.listdir(base_path)
    xml_list = [x for x in base_list if x.lower().endswith(('xml')) and x.lower().startswith(('0'))]
    xml_list.sort()
    json_list = [x for x in base_list if x.lower().endswith(('json')) and x.lower().startswith(('0'))]
    json_list.sort()


    #vis_mask(rgb_path, dp_path, xml_list, json_list, seq, record_video_flag=False, depth_threshold=args.depth_threshold)
    vis_mask(rgb_path, dp_path, xml_list, json_list, seq, record_video_flag=False)