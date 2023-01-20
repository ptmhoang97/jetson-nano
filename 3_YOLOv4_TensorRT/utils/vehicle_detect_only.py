import cv2
import math

def is_old(center_Xd, center_Yd, tracker_elements, img_copy):
    height = img_copy.shape[0]
    width = img_copy.shape[1]
    max_distance = 20
    flg_is_old = False
    for idx_ele,ele in enumerate(tracker_elements):
        box_t_coordinate = ele[1]
        (xt, yt, wt, ht) = [int(c) for c in box_t_coordinate]
        center_Xt, center_Yt = int((xt + (xt + wt)) / 2.0), int((yt + (yt + ht)) / 2.0)
        distance = math.sqrt((center_Xt - center_Xd) ** 2 + (center_Yt - center_Yd) ** 2)
        
        # red car, video3, detect and track, MOSSE
        # temp_idx = [2,4,5]
        # red car, video3, detect and track, MedianFlow
        # temp_idx = [2]
        # red car, video3, detect only
        temp_idx = [2,29,30,35,37]
        
        if ele[0] in temp_idx and distance <= max_distance:
            print(ele[0],center_Xd,center_Yd,center_Xt,center_Yt,distance)
        
        if center_Yt < height*0.6:
            max_distance = 20
        if distance <= max_distance:
            flg_is_old = True
            return flg_is_old, idx_ele
    return flg_is_old, -1
    
obj_cnt = 0
curr_trackers = []

def vehicle_detect_only(trt_yolo,img_copy,conf_th,frame_count):
    global obj_cnt,curr_trackers
    tracker_elements = []
    # First frame, detect and track
    if frame_count == 1:
        # Get properties of all vehicle in frame after detection
        boxes_d, confs, clss = trt_yolo.detect(img_copy, conf_th)
        # Loop each vehicle for tracking
        for idx,box_d in enumerate(boxes_d):
            x1,y1,x2,y2 = box_d
            box_tmp = [0,0,0,0]
            box_tmp[0] = int(x1)
            box_tmp[1] = int(y1)
            box_tmp[2] = int(x2-x1)
            box_tmp[3] = int(y2-y1)
            
            obj_cnt += 1
            
            new_obj = dict()
            new_obj['tracker_id'] = obj_cnt
            new_obj['box_d'] = box_tmp
            new_obj['tracker_confidence'] = confs[idx]
            new_obj['tracker_class'] = clss[idx]

            curr_trackers.append(new_obj)
    # After first frame, detect and track
    else:
        # Loop old vehicle to perform tracking
        old_trackers = curr_trackers
        curr_trackers = []

        for car in old_trackers:
            # Update tracker
            box_d = car['box_d']
            tracker_id = car['tracker_id']
            tracker_conf = car['tracker_confidence']
            tracker_cls = car['tracker_class']

            tracker_elements.append([tracker_id,box_d,tracker_conf,tracker_cls])
            
        boxes_d, confs, clss = trt_yolo.detect(img_copy, conf_th)
        print("go",frame_count-1,frame_count)
        for idx,box_d in enumerate(boxes_d):
            x1,y1,x2,y2 = box_d
            box_tmp = [0,0,0,0]
            box_tmp[0] = int(x1)
            box_tmp[1] = int(y1)
            box_tmp[2] = int(x2-x1)
            box_tmp[3] = int(y2-y1)
            center_Xd = int((x1+x2)/2)
            center_Yd = int((y1+y2)/2)
            flg_is_old, idx_box_t = is_old(center_Xd, center_Yd, tracker_elements, img_copy)
            if not flg_is_old:
                obj_cnt += 1
            
                new_obj = dict()
                new_obj['tracker_id'] = obj_cnt
                new_obj['box_d'] = box_tmp
                new_obj['tracker_confidence'] = confs[idx]
                new_obj['tracker_class'] = clss[idx]

                curr_trackers.append(new_obj)
            else:
                box_t_track_id = tracker_elements[idx_box_t][0]

                new_obj = dict()
                new_obj['tracker_id'] = box_t_track_id
                new_obj['box_d'] = box_tmp
                new_obj['tracker_confidence'] = confs[idx]
                new_obj['tracker_class'] = clss[idx]

                curr_trackers.append(new_obj)
    return tracker_elements
