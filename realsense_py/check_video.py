#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
from tkinter import *
import tkinter.filedialog
import time
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

if __name__ == '__main__':
    #input_path = os.path.join(args.save_path, args.input)
    # save_path = os.path.join(args.save_path, '%s/%s' % (args.group_id, args.input))
    root = Tk()
    root.withdraw()
    filename = tkinter.filedialog.askopenfilename()
    save_path = os.path.dirname(filename)
    pre_filename = os.path.splitext(os.path.basename(filename))[0]

    try:
        pipeline = rs.pipeline()

        # Create a config object
        config = rs.config()

        # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
        rs.config.enable_device_from_file(config, filename)

        # Configure the pipeline to stream the depth stream
        # Change this parameters according to the recorded bag file resolution
        config.enable_stream(rs.stream.depth, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, rs.format.rgb8, 30)

        # Start streaming from file
        pipeline.start(config)

        # Create an align object
        align_to = rs.stream.color
        align = rs.align(align_to)

        # Create colorizer object
        colorizer = rs.colorizer()

        # Streaming loop
        while True:
            # Get frameset of depth
            try:
                frames = pipeline.wait_for_frames(300)
            except RuntimeError as e:
                print(e)
                print('finished')
                break

            # Get depth frame
            aligned_frames = align.process(frames)
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            # Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                continue

            depth_image = np.asanyarray(aligned_depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Render images
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            # convert grb to rgb
            color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            images = np.hstack((color_image, depth_colormap))  # display horizontal
            cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Align Example', images)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        pass

