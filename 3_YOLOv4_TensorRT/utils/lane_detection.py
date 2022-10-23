# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 14:06:29 2021

@author: OAM81HC
"""
import cv2
import numpy as np
import math

def get_video_name(vid_name):
    global video_name
    video_name = vid_name
    
def get_x_top_center_region_detect_lane(img):
    region_of_lane_line = region_detect_lane(img)
    region_of_lane_line = region_of_lane_line.tolist()
    region_x_top_left_point = region_of_lane_line[0][1][0]
    region_x_top_right_point = region_of_lane_line[0][2][0]
    region_x_top_center_point = int((region_x_top_left_point+region_x_top_right_point)/2)
    return region_x_top_center_point
    
def region_detect_lane(img):
    height = img.shape[0]
    width = img.shape[1]
    
    global video_name
    
    if video_name == "video1.mp4":
        pt_left_bot_width = 0.05
        pt_left_bot_height = 1
        pt_left_top_width = 0.45
        pt_left_top_height = 0.6
        pt_right_top_width = 0.55
        pt_right_top_height = 0.6
        pt_right_bot_width = 0.95
        pt_right_bot_height = 1
    elif video_name == "video2.mp4":
        pt_left_bot_width = 0.3
        pt_left_bot_height = 1
        pt_left_top_width = 0.45
        pt_left_top_height = 0.7
        pt_right_top_width = 0.55
        pt_right_top_height = 0.7
        pt_right_bot_width = 0.8
        pt_right_bot_height = 1
    elif video_name == "video3.mp4":
        pt_left_bot_width = 0.12
        pt_left_bot_height = 0.8
        pt_left_top_width = 0.28
        pt_left_top_height = 0.6
        pt_right_top_width = 0.5
        pt_right_top_height = 0.6
        pt_right_bot_width = 0.7
        pt_right_bot_height = 0.8
    elif video_name == "video4.mp4":
        pt_left_bot_width = 0.3
        pt_left_bot_height = 0.7
        pt_left_top_width = 0.43
        pt_left_top_height = 0.55
        pt_right_top_width = 0.63
        pt_right_top_height = 0.55
        pt_right_bot_width = 0.85
        pt_right_bot_height = 0.7
    elif video_name == "video5.mp4":
        pt_left_bot_width = 0.12
        pt_left_bot_height = 0.8
        pt_left_top_width = 0.32
        pt_left_top_height = 0.6
        pt_right_top_width = 0.6
        pt_right_top_height = 0.6
        pt_right_bot_width = 0.75
        pt_right_bot_height = 0.8
    else:
        pass
    
    region_of_lane_line = np.array([[
        (width*pt_left_bot_width, height*pt_left_bot_height),
        (width*pt_left_top_width, height*pt_left_top_height),
        (width*pt_right_top_width, height*pt_right_top_height),
        (width*pt_right_bot_width, height*pt_right_bot_height),]], np.int32)
        
    return region_of_lane_line

def canny(img):
    if img is None:
        cap.release()
        cv2.destroyAllWindows()
        exit()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)

    canny = cv2.Canny(gray, 100, 200)
    return canny

def region_of_interest_gray(img):
    region_of_lane_line = region_detect_lane(img)
    
    mask = np.zeros_like(img)
    
    cv2.fillPoly(mask, region_of_lane_line, 255)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def houghLines(cropped_canny):
    return cv2.HoughLinesP(cropped_canny, 1, np.pi/180, 20,
                           np.array([]), minLineLength=15, maxLineGap=20)

def addWeighted(frame, line_image):
    # return frame
    return cv2.addWeighted(frame, 1, line_image, 1, 1)
    
def addWeighted2(img):
    img_copy = img.copy()
    
    height = img_copy.shape[0]
    width = img_copy.shape[1]

    mask = np.zeros_like(img)
    
    region_of_lane_line = region_detect_lane(img)
    cv2.fillPoly(mask, region_of_lane_line, 255)
    
    img = cv2.addWeighted(img, 1, mask, 0.5, 1)
    
    for i in range(1,10):
        cv2.line(img,(int(width*i/10),0),(int(width*i/10),height),(255,255,0),5)
        
    return img
    
def scale_display_line():
    global video_name
    
    if video_name == "video1.mp4":
        scale_y1 = 1
        scale_y2 = 0.65
    elif video_name == "video2.mp4":
        scale_y1 = 1
        scale_y2 = 0.7
    elif video_name == "video3.mp4":
        scale_y1 = 0.8
        scale_y2 = 0.55
    elif video_name == "video4.mp4":
        scale_y1 = 0.7
        scale_y2 = 0.55
    elif video_name == "video5.mp4":
        scale_y1 = 0.8
        scale_y2 = 0.6
    else:
        pass
    
    return scale_y1,scale_y2

def display_lines(img, lines):
    line_image = np.zeros_like(img)
    scale_y1,scale_y2 = scale_display_line()
    y_max = int(img.shape[0]*scale_y1)
    y_min = int(img.shape[0]*scale_y2)
    if lines is not None:
        fill_gap = []
        for i,line in enumerate(lines):
            x1, y1, x2, y2 = line
            fill_gap.append(line)

            if i == 1:
                point_1 = fill_gap[0][0:2]
                point_2 = fill_gap[0][2:4]
                point_3 = fill_gap[1][2:4]
                point_4 = fill_gap[1][0:2]
                
                cv2.line(line_image, (point_1[0], point_1[1]), (point_2[0], point_2[1]), (0, 0, 255), 10)
                cv2.line(line_image, (point_3[0], point_3[1]), (point_4[0], point_4[1]), (0, 0, 255), 10)
                
                fill_gap = [point_1] + [point_2] + [point_3] + [point_4]

                fill_gap_np = np.array(fill_gap,dtype=(np.int32)).reshape(1,4,2)
                
                cv2.fillPoly(line_image, fill_gap_np, (0,225,0))
    return line_image

def make_points(image, line):
    slope, intercept = line
    
    scale_y1,scale_y2 = scale_display_line()
        
    y1 = int(image.shape[0]*scale_y1)
    y2 = int(image.shape[0]*scale_y2)
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    
    min_angle = math.tan(math.pi*20/180)
    max_angle = math.tan(math.pi*70/180)

    region_x_top_center_point = get_x_top_center_region_detect_lane(image)

    if lines is None:
        return None

    for line in lines:
        for x1, y1, x2, y2 in line:
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]

            if slope < 0:
                if min_angle < abs(slope) < max_angle:
                    if all(x < region_x_top_center_point for x in(x1,x2)):
                        left_fit.append((slope, intercept))
            else:
                if min_angle < abs(slope) < max_angle:
                    if all(x > region_x_top_center_point for x in(x1,x2)):
                        right_fit.append((slope, intercept))
                    
    if len(left_fit) !=  0 and len(right_fit) != 0:
        left_fit_average = np.average(left_fit, axis=0)
        left_line = make_points(image, left_fit_average)
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_points(image, right_fit_average)
        
        
        if min_angle < abs(left_fit_average[0]) < max_angle:
            if all(x < region_x_top_center_point for x in(left_line[0],left_line[2])):
                left_line = left_line
            else:
                left_line = None 
        
        if min_angle < abs(right_fit_average[0]) < max_angle:
            if all(x > region_x_top_center_point for x in(right_line[0],right_line[2])):
                right_line = right_line
            else:
                right_line = None
        
        if left_line is not None and right_line is not None:
            averaged_lines = [left_line,right_line]
        elif left_line is not None:
            averaged_lines = [left_line,None]
        elif right_line is not None:
            averaged_lines = [None,right_line]
        else:
            averaged_lines = None
    elif len(right_fit) != 0:
        right_fit_average = np.average(right_fit, axis=0)
        right_line = make_points(image, right_fit_average)
        
        if min_angle < abs(right_fit_average[0]) < max_angle:
            if all(x > region_x_top_center_point for x in(right_line[0],right_line[2])):
                right_line = right_line
            else:
                right_line = None
        
        if right_line is not None:
            averaged_lines = [None,right_line]
        else:
            averaged_lines = None
    elif len(left_fit) !=  0:
        left_fit_average = np.average(left_fit, axis=0)
        left_line = make_points(image, left_fit_average)
        
        if min_angle < abs(left_fit_average[0]) < max_angle:
            if all(x < region_x_top_center_point for x in(left_line[0],left_line[2])):
                left_line = left_line
            else:
                left_line = None
        
        if left_line is not None:
            averaged_lines = [left_line,None]
        else:
            averaged_lines = None
    else:
        averaged_lines = None

    return averaged_lines

total_frame = 0
counter_frame_after_detect_lane_first_time = 0
frame_2_lines = 0
percent_2_lines = 0
backup_averaged_lines = [None,None]
video_name = ""
is_lane_detect_first_time = False
def lane_detection(frame):
    global total_frame
    global frame_2_lines
    global percent_2_lines
    global backup_averaged_lines
    global is_lane_detect_first_time
    global counter_frame_after_detect_lane_first_time

    total_frame += 1

    if (backup_averaged_lines[0] is not None) and (backup_averaged_lines[1] is not None):
        is_lane_detect_first_time = True
    
    if is_lane_detect_first_time is False:
        canny_image = canny(frame)
        cropped_canny = region_of_interest_gray(canny_image)
        lines = houghLines(cropped_canny)
        averaged_lines = average_slope_intercept(frame, lines)
    else:
        counter_frame_after_detect_lane_first_time+=1
        if counter_frame_after_detect_lane_first_time%5 == 0:
            canny_image = canny(frame)
            cropped_canny = region_of_interest_gray(canny_image)
            lines = houghLines(cropped_canny)
            averaged_lines = average_slope_intercept(frame, lines)
        else:
            averaged_lines = None
            pass

    # New lane line detection (if left line or right line is not detected, it will be filled with backup line)
    if averaged_lines is not None:
        if (averaged_lines[0] is not None) and (averaged_lines[1] is not None):
            backup_averaged_lines[0] = averaged_lines[0]
            backup_averaged_lines[1] = averaged_lines[1]
            line_image = display_lines(frame, averaged_lines)
            combo_image = addWeighted(frame, line_image)
        elif (averaged_lines[0] is None) and (averaged_lines[1] is not None):
            backup_averaged_lines[1] = averaged_lines[1]
            if backup_averaged_lines[0] is None:
                averaged_lines.pop(0)
                line_image = display_lines(frame, averaged_lines)
                combo_image = addWeighted(frame, line_image)
            else:
                averaged_lines[0] = backup_averaged_lines[0]
                line_image = display_lines(frame, averaged_lines)
                combo_image = addWeighted(frame, line_image)
        elif (averaged_lines[0] is not None) and (averaged_lines[1] is None):
            backup_averaged_lines[0] = averaged_lines[0]
            if backup_averaged_lines[1] is None:
                averaged_lines.pop(1)
                line_image = display_lines(frame, averaged_lines)
                combo_image = addWeighted(frame, line_image)
            else:
                averaged_lines[1] = backup_averaged_lines[1]
                line_image = display_lines(frame, averaged_lines)
                combo_image = addWeighted(frame, line_image)
        elif (averaged_lines[0] is None) and (averaged_lines[1] is None):
            pass
        else:
            pass
            
        if len(averaged_lines) == 2:
            frame_2_lines += 1
        else:
            pass
    else:
        if (backup_averaged_lines[0] is None) and (backup_averaged_lines[1] is None):
            combo_image = frame
        elif (backup_averaged_lines[0] is not None) and (backup_averaged_lines[1] is not None):
            line_image = display_lines(frame, backup_averaged_lines)
            combo_image = addWeighted(frame, line_image)
        elif (backup_averaged_lines[0] is None) and (backup_averaged_lines[1] is not None):
            line_image = display_lines(frame, [backup_averaged_lines[1]])
            combo_image = addWeighted(frame, line_image)
        elif (backup_averaged_lines[0] is not None) and (backup_averaged_lines[1] is None):
            line_image = display_lines(frame, [backup_averaged_lines[0]])
            combo_image = addWeighted(frame, line_image)
        else:
            pass
    
    percent_2_lines = round((frame_2_lines/total_frame*100),2)
    # print("percent 2 lines: ", percent_2_lines, frame_2_lines, total_frame)
    
    # Enable straight line in window to choose the scale interest region
    # combo_image = addWeighted2(combo_image)
    
    return averaged_lines, combo_image
