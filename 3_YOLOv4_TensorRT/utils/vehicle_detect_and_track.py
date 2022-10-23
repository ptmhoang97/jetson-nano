import cv2
import math
    
def is_old(center_Xd, center_Yd, tracker_elements):
    max_distance = 50
    flg_is_old = False
    for idx_ele,ele in enumerate(tracker_elements):
        box_t_coordinate = ele[1]
        (xt, yt, wt, ht) = [int(c) for c in box_t_coordinate]
        center_Xt, center_Yt = int((xt + (xt + wt)) / 2.0), int((yt + (yt + ht)) / 2.0)
        distance = math.sqrt((center_Xt - center_Xd) ** 2 + (center_Yt - center_Yd) ** 2)

        if distance < max_distance:
            flg_is_old = True
            return flg_is_old, idx_ele
    return flg_is_old, -1

def create_tracker():
    # tracker = cv2.legacy.TrackerKCF_create()
    # tracker = cv2.legacy.TrackerMedianFlow_create()
    tracker = cv2.legacy.TrackerMOSSE_create()

    return tracker
    
obj_cnt = 0
curr_trackers = []

def vehicle_detect_and_track(trt_yolo,img_copy,conf_th,frame_count):
    global obj_cnt,curr_trackers
    tracker_elements = []
    # First frame, detect and track
    if frame_count == 1:
        # Get properties of all vehicle in frame after detection
        boxes_detect, confs, clss = trt_yolo.detect(img_copy, conf_th)
        # Loop each vehicle for tracking
        for idx,box_d in enumerate(boxes_detect):
            x1,y1,x2,y2 = box_d
            box_tmp = [0,0,0,0]
            box_tmp[0] = int(x1)
            box_tmp[1] = int(y1)
            box_tmp[2] = int(x2-x1)
            box_tmp[3] = int(y2-y1)
            
            tracker = create_tracker()
            tracker.init(img_copy, tuple(box_tmp))
        
            obj_cnt += 1
            
            new_obj = dict()
            new_obj['tracker_id'] = obj_cnt
            new_obj['tracker'] = tracker
            new_obj['tracker_confidence'] = confs[idx]
            new_obj['tracker_class'] = clss[idx]

            curr_trackers.append(new_obj)
    # After first frame, detect and track
    else:
        # Loop old vehicle to perform tracking
        old_trackers = curr_trackers
        curr_trackers = []
        tracker_elements = []
        for car in old_trackers:
            # Update tracker
            tracker = car['tracker']
            tracker_id = car['tracker_id']
            tracker_conf = car['tracker_confidence']
            tracker_cls = car['tracker_class']
            (success, box_t) = tracker.update(img_copy)

            if success:
                tracker_elements.append([tracker_id,box_t,tracker_conf,tracker_cls])
                new_obj = dict()
                new_obj['tracker_id'] = tracker_id
                new_obj['tracker'] = tracker
                new_obj['tracker_confidence'] = tracker_conf
                new_obj['tracker_class'] = tracker_cls
                
                # track tiep
                curr_trackers.append(new_obj)
        
        # After every 15 frame, we will perform detection and update tracker again
        if frame_count % 15 == 0:
            boxes_detect, confs, clss = trt_yolo.detect(img_copy, conf_th)
            for idx,box_d in enumerate(boxes_detect):
                x1,y1,x2,y2 = box_d
                box_tmp = [0,0,0,0]
                box_tmp[0] = int(x1)
                box_tmp[1] = int(y1)
                box_tmp[2] = int(x2-x1)
                box_tmp[3] = int(y2-y1)
                center_Xd = int((x1+x2)/2)
                center_Yd = int((y1+y2)/2)
                flg_is_old, idx_box_t = is_old(center_Xd, center_Yd, tracker_elements)
                if not flg_is_old:
                    tracker = create_tracker()
                    tracker.init(img_copy, tuple(box_tmp))
                    
                    obj_cnt += 1

                    new_obj = dict()
                    new_obj['tracker_id'] = obj_cnt
                    new_obj['tracker'] = tracker
                    new_obj['tracker_confidence'] = confs[idx]
                    new_obj['tracker_class'] = clss[idx]

                    curr_trackers.append(new_obj)
                else:
                    box_t_track_id = tracker_elements[idx_box_t][0]
                    for tracker_tmp in curr_trackers:
                        if tracker_tmp['tracker_id'] == box_t_track_id:
                            tracker = create_tracker()
                            tracker.init(img_copy, tuple(box_tmp))
                            tracker_tmp['tracker'] = tracker
                            tracker_tmp['tracker_confidence'] = confs[idx]
                            tracker_tmp['tracker_class'] = clss[idx]
    return tracker_elements
