#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
import time
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path
from tkinter import *
import tkinter.filedialog


if __name__ == '__main__':
    root = Tk()
    root.withdraw()
    filename = tkinter.filedialog.askopenfilename()
    save_dir_path = os.path.dirname(filename)

    # save png file path
    save_path = os.path.join(save_dir_path, '%s' %  time.strftime("%y%m%d-%H%M%S"))
    print("save path:", save_path)

    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    if not os.path.isdir(os.path.join(save_path, 'color')):
        os.mkdir(os.path.join(save_path, 'color'))

    if not os.path.isdir(os.path.join(save_path, 'depth')):
        os.mkdir(os.path.join(save_path, 'depth'))

    if not os.path.isdir(os.path.join(save_path, 'colormap')):
        os.mkdir(os.path.join(save_path, 'colormap'))
    # Png index
    index = 0

    try:
        pipeline = rs.pipeline()

        # Create a config object
        config = rs.config()

        # Tell config that we will use a recorded device from file to be used by the pipeline.
        rs.config.enable_device_from_file(config, filename, repeat_playback=False)

        # Configure the pipeline to stream the depth stream
        # Change this parameters according to the recorded bag file resolution
        config.enable_stream(rs.stream.depth, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, rs.format.rgb8, 30)

        # Start streaming from file
        pipeline.start(config)

        # Create opencv window to render image in
        cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)

        # Create an align object
        align_to = rs.stream.color
        align = rs.align(align_to)

        # Create colorizer object
        colorizer = rs.colorizer()

        # Streaming loop
        while True:
            # Get frameset of depth
            try:
                frames = pipeline.wait_for_frames(2000)
            except RuntimeError as e:
                # print(e)
                print("Finished, please check the png file output: color, colormap and depth")
                print("each subdirectory has ", '%d' % index, " png files (video 30fps)")
                break

            # frames = pipeline.wait_for_frames()

            # Get depth frame
            aligned_frames = align.process(frames)
            # depth_frame = frames.get_depth_frame()

            # Colorize depth frame to jet colormap
            # depth_color_frame = colorizer.colorize(depth_frame)
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())


            # Render images
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET)


            # convert grb to rgb
            color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
     

            # save png file
            cv2.imwrite('%s/%s/%08d_color.png' % (save_path, 'color', index), color_image_rgb)
            cv2.imwrite('%s/%s/%08d_depth.png' % (save_path, 'depth', index), depth_image)
            cv2.imwrite('%s/%s/%08d_colormap.png' % (save_path, 'colormap', index), depth_colormap)
            index += 1
    finally:
        pass

