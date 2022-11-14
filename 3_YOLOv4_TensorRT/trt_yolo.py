"""trt_yolo.py

This script demonstrates how to do real-time object detection with
TensorRT optimized YOLO engine.
"""


import os
import time
import argparse

import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver

from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
from utils.lane_detection import lane_detection
from utils.vehicle_detect_and_track import vehicle_detect_and_track
from utils.track_vehicle_change_lane import track_vehicle_change_lane
from utils.prepare_input_for_display import prepare_input_for_display
from utils.vehicle_detect_only import vehicle_detect_only

WINDOW_NAME = 'TrtYOLODemo'


def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'YOLO model on Jetson')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_camera_args(parser)
    parser.add_argument(
        '-c', '--category_num', type=int, default=80,
        help='number of object categories [80]')
    parser.add_argument(
        '-m', '--model', type=str, required=True,
        help=('[yolov3-tiny|yolov3|yolov3-spp|yolov4-tiny|yolov4|'
              'yolov4-csp|yolov4x-mish]-[{dimension}], where '
              '{dimension} could be either a single number (e.g. '
              '288, 416, 608) or 2 numbers, WxH (e.g. 416x256)'))
    parser.add_argument(
        '-l', '--letter_box', action='store_true',
        help='inference with letterboxed image [False]')
    args = parser.parse_args()
    return args
    
def loop_detect_and_track(cam, trt_yolo, conf_th, vis, vid_name):
    """Continuously capture images from camera and do object detection.

    # Arguments
      cam: the camera instance (video source).
      trt_yolo: the TRT YOLO object detector instance.
      conf_th: confidence/score threshold for object detection.
      vis: for visualization.
    """
    full_scrn = False
    fps = 0.0
    tic = time.time()
    
    frame_count = 0
    frame_match_count = 0
    stop_each_frame = 0
    while True:
        if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
            break
        img = cam.read()
        
        if img is None:
            break

        img_copy = img.copy()
        
        # Frame counter
        frame_count+=1

        # Vehicle detection and tracking
        tracker_elements = vehicle_detect_and_track(trt_yolo, img, conf_th, frame_count)
        
        # Vehicle detection only
        # tracker_elements = vehicle_detect_only(trt_yolo, img_copy, conf_th, frame_count)

        # Track vehicle change lane
        tracker_change_lane = track_vehicle_change_lane(vid_name, img_copy, tracker_elements, frame_count)

        # lane detection and display lane
        averaged_lines, img = lane_detection(img)

        # Display properties of vehicle (bounding box, changing lane status, track id)
        if len(tracker_change_lane) != 0:
            tracker_elements_draw = prepare_input_for_display(img_copy,tracker_change_lane)
            img = vis.draw_bboxes(img, tracker_elements_draw)

        # display fps
        img = show_fps(img, fps, frame_count)
        
        for ele in tracker_elements:
            # red car, video3, detect and track, MOSSE
            # temp_idx = [2,4,5]
            # red car, video3, detect and track, MedianFlow
            # temp_idx = [2]
            # red car, video3, detect only
            # temp_idx = [2,29,30,35,37]
            
            # orange car, video3, detect and track, MOSSE
            # temp_idx = [1]
            # orange car, video3, detect and track, MedianFlow
            # temp_idx = [1,3]
            # orange car, video3, detect only
            temp_idx = [1]
            
            if ele[0] in temp_idx:
                frame_match_count += 1
                break
        # print("Percent detect",round(frame_match_count/frame_count*100,2))
        # print("Percent detect",round(frame_match_count/250*100,2))
        cv2.imshow(WINDOW_NAME, img)
        
        # calculate fps
        toc = time.time()
        curr_fps = 1.0 / (toc - tic)
        fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
        tic = toc
        
        if stop_each_frame == 1:
            while True:
                key = cv2.waitKey(1)
                if key == ord('s'): # r key: resume program
                    break
                elif key == ord('d'): # r key: resume program
                    stop_each_frame = 0
                    break
        
        # keyboard check
        key = cv2.waitKey(1)
        if key == 27:  # ESC key: quit program
            break
        elif key == ord('e'): # e key: pause program
            while True:
                key = cv2.waitKey(1)
                if key == ord('r'): # r key: resume program
                    break
        elif key == ord('a'): # e key: pause program
            while True:
                key = cv2.waitKey(1)
                if key == ord('s'): # r key: resume program
                    stop_each_frame = 1
                    break
        
def main():
    args = parse_args()
    if args.category_num <= 0:
        raise SystemExit('ERROR: bad category_num (%d)!' % args.category_num)
    if not os.path.isfile('yolo/%s.trt' % args.model):
        raise SystemExit('ERROR: file (yolo/%s.trt) not found!' % args.model)

    cam = Camera(args)
    if not cam.isOpened():
        raise SystemExit('ERROR: failed to open camera!')
    
    cls_dict = get_cls_dict(args.category_num)
    vis = BBoxVisualization(cls_dict)
    trt_yolo = TrtYOLO(args.model, args.category_num, args.letter_box)

    open_window(
        WINDOW_NAME, 'Camera TensorRT YOLO Demo',
        cam.img_width, cam.img_height)
    loop_detect_and_track(cam, trt_yolo, conf_th=0.3, vis=vis, vid_name = args.video)

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
