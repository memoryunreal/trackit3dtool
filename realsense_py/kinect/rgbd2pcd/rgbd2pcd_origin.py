import os
import argparse
import shutil
from typing import DefaultDict

import numpy as np
import open3d as o3d
from PIL import Image
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import filedialog

def file_exist(file_path, ext=''):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return False
    elif ext in os.path.splitext(file_path)[1] or not ext:
        return True
    return False

def align_color2depth(o3d_color, o3d_depth):
    color_data = np.asarray(o3d_color)
    depth_data = np.asarray(o3d_depth)
    scale = [np.shape(depth_data)[0]/np.shape(color_data)[0], \
        np.shape(depth_data)[1]/np.shape(color_data)[1]]
    if scale != [1.0, 1.0]:
        color = Image.fromarray(color_data)
        depth = Image.fromarray(depth_data)
        color = color.resize(depth.size)
        return o3d.geometry.Image(np.asarray(color)), scale, np.shape(depth_data)
    return o3d_color, scale, np.shape(depth_data)

def get_intrinsic(intrinsic_str, width, height, scale=[1.0, 1.0]):
    if not intrinsic_str:
        return o3d.camera.PinholeCameraIntrinsic( \
            o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
    intrinsic = np.fromstring(intrinsic_str[1:-1], dtype=np.float, sep=',')
    intrinsic = intrinsic.reshape(3, 3).transpose()
    scale = np.append(scale, 1.0)
    intrinsic = np.matmul(np.diag(scale), intrinsic)
    intrinsic = intrinsic.flatten('F').tolist()
    return o3d.camera.PinholeCameraIntrinsic(width, height, \
        intrinsic[0], intrinsic[4], intrinsic[6], intrinsic[7])


def getFiles(directory_name):
    array_of_img = []
    for filename in os.listdir(directory_name):
        img = o3d.io.read_image(directory_name + "/" + filename)
        array_of_img.append(img)
    return array_of_img


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        print
        path + ' εε»Ίζε'
        return True
    else:
        print
        path + ' η?ε½ε·²ε­ε¨'
        return False

def cover_files(source_dir, target_ir):
    for file in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file)
        if os.path.isfile(source_file):
            shutil.copy(source_file, target_ir)


def configure(args):
    if not file_exist(args.color):
        print(f'ERROR: Cannot open file {args.color}')
        return False
    if not file_exist(args.depth):
        print(f'ERROR: Cannot open file {args.depth}')
        return False
    if not os.path.splitext(args.color)[1] in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
        print(f'ERROR: File extension {os.path.splitext(args.color)[1]} is not supported')
        return False
    if not os.path.splitext(args.depth)[1] in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
        print(f'ERROR: File extension {os.path.splitext(args.depth)[1]} is not supported')
        return False
    if args.output and not file_exist(args.output):
        print(f'ERROR: Cannot write file {args.output}')
        return False
    return True
    

def main(args):

    # color = o3d.io.read_image(args.color)
    # depth = o3d.io.read_image(args.depth)
    path = args.sequence + 'image/color/'
    mkdir(path)
    cover_files(args.sequence+'color/', path)
    path_calib = args.sequence + 'calib/'
    mkdir(path_calib)
    cover_files(args.data+'calib/', path_calib)
    path2 = args.sequence + 'pcd/'
    mkdir(path2)
    path3 = args.sequence + 'label/'
    mkdir(path3)
    colorx = getFiles(args.color)
    depthx = getFiles(args.depth)
    pcd_name = []
    dataname = os.listdir(args.color)
    for i in dataname:
        # file_num1, file_num2, file_num3 = os.path.splitext(i)[0].partition("_")
        # pcd_name.append(file_num1)
        file_num = os.path.splitext(i)[0]
        pcd_name.append(file_num)
        pcd_file = open(args.sequence + 'pcd/' + file_num + '.pcd', 'w')
        pcd_file.close()


    for i in range(0, len(colorx)):
        color = colorx[i]
        depth = depthx[i]
        if args.view_depth:
            depth_data = np.asarray(depth)
            depth_data = depth_data.astype('float') / 1000
            cm = plt.get_cmap('jet')
            color_depth = cm(depth_data / 3.0)
            color_depth *= 255
            color_depth = color_depth.astype('uint8')
            plt.imshow(color_depth)
            plt.show()
        color, scale, shape = align_color2depth(color, depth)
        assert color, "ERROR: Empty color image"
        assert depth, "ERROR: Empty depth image"
        assert len(scale) == 2, "ERROR: Wrong scale during align color to depth"
        intrinsic = get_intrinsic(args.intrinsic, shape[0], shape[1], scale)
        if args.no_color:
            pcd = o3d.geometry.PointCloud.create_from_depth_image(depth, intrinsic)
        else:
            rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth( \
                color, depth, depth_trunc=10.0, convert_rgb_to_intensity=False)
            pcd = o3d.geometry.PointCloud.create_from_rgbd_image( \
                rgbd, intrinsic)
        if args.downsampling:
            print("Downsampling the point cloud with a voxel of 0.05")
            downpcd = pcd.voxel_down_sample(voxel_size=0.05)
            o3d.visualization.draw_geometries([downpcd])
        if args.show:
            pcd1 = o3d.io.read_point_cloud(args.show)
            o3d.visualization.draw_geometries([pcd1])
        # if args.output:
        #     o3d.io.write_point_cloud(args.output, pcd)
        #     print('successful write the o.pcd file')

        # Flip pcd, otherwise will be upside down
        # pcd.transform(np.diag([1, -1, -1, 1]))
        # R = pcd.get_rotation_matrix_from_xyz((np.pi/2,0,0))
        # pcd.rotate(R, center=(0, 0, 0))
        # if args.view:
        #     vis = o3d.visualization.Visualizer()
        #     vis.create_window(window_name='View', width=640, height=480, visible=True)
        #     vis.add_geometry(pcd)
        #     vis.run()
        #     vis.destroy_window()
        if args.view:
            o3d.visualization.draw_geometries([pcd])
        o3d.io.write_point_cloud(args.sequence + 'pcd/' + pcd_name[i]+'.pcd', pcd)
        out = pcd_name[i]
        print(out)
    print('successful write the o.pcd file')







if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert RGBD images to a point cloud!')
    parser.add_argument('-c', '--color', dest='color', action='store', required=True, \
        help='Input RGB color image')
    parser.add_argument('-d', '--depth', dest='depth', action='store', required=True, \
        help='Input depth map')
    parser.add_argument('-da', '--data', dest='data', action='store', required=True, \
                        help='Input data path')
    parser.add_argument('-seq', '--sequence', dest='sequence', action='store', required=True, \
                        help='Input sequence path')


    parser.add_argument('-i', '--intrinsic', dest='intrinsic', action='store', type=str, required=False, \
        default="[540.7, 0, 0, 0, 540.7, 0, 478.8, 269.8, 1]", \
        help='Camera intrinsic parameters')
    parser.add_argument('-nv', '--no_view', dest='view', default=False, action='store_false', required=False, \
        help='Disable point cloud visualization')
    parser.add_argument('-nc', '--no_color', dest='no_color', default=False, action='store_true', required=False, \
        help='Only use depth image')
    parser.add_argument('-vd', '--view_depth', dest='view_depth', default=False, action='store_true', required=False, \
        help='Visualize color mapped depth image')
    # parser.add_argument('-o', '--output', dest='output', action='store', required=False, \
    #     help='Output point cloud file path')
    parser.add_argument('-s', '--show', dest='show', action='store', required=False, \
                        help='Show point cloud file path')
    parser.add_argument('-dw', '--downsampling', dest='downsampling', default=False, action='store_true', required=False, \
                        help='Downsampling point cloud')

    args = parser.parse_args()
    root = Tk()
    root.withdraw()
    dirpath = filedialog.askdirectory(initialdir='/media/silence/DataT')

  
    # if not configure(args):
    #     exit(0)

    main(args)