from utils.lane_detection import get_video_name,get_x_top_center_region_detect_lane

tracker_change_lane = []
def track_vehicle_change_lane(vid_name, img, tracker_elements, frame_count):
    global tracker_change_lane
    # Get input video name
    get_video_name(vid_name)
    
    # Get x coordinate of center point between 2 two point of region detect lane
    region_x_top_center_point = get_x_top_center_region_detect_lane(img)
    
    # Create some temporary array to store properties of current detection and tracking
    tracker_id = []
    distance = []
    boxes = []
    confs = []
    clss = []
    for ele in tracker_elements:
        tracker_id.append(ele[0])
        x = ele[1][0]
        y = ele[1][1]
        w = ele[1][2]
        h = ele[1][3]
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        vehicle_x_center = (x1+x2)/2
        vehicle_y_center = (y1+y2)/2
        dist = abs(int(region_x_top_center_point - vehicle_x_center))
        distance.append(dist)
        boxes.append([x1,y1,x2,y2])
        confs.append(ele[2])
        clss.append(ele[3])

    # If backup tracking array for store current tracking properties equal zero (so this is first time)
    if len(tracker_change_lane) == 0:
        # Proceed storing properties for first time
        for trk_id, dist, bb, cf, cl in zip(tracker_id, distance, boxes, confs, clss):
            # If distance between center of vehicle bounding box and center of lane < 5 pixel,
            # we will not track that vehicle.
            if dist < 50:
                pass
            # Start tracking this vehicle
            else:
                temp_dict = dict()
                temp_dict['tracker_id'] = trk_id
                temp_dict['distance'] = dist
                temp_dict['change_lane_counter'] = 0
                temp_dict['no_change_lane_counter'] = 0
                temp_dict['frame_exist_vehicle'] = frame_count
                temp_dict['change_lane_flg'] = False
                temp_dict['inside_lane_flg'] = False
                temp_dict['boxes'] = bb
                temp_dict['confs'] = cf
                temp_dict['clss'] = cl
                tracker_change_lane.append(temp_dict)
                
    # Tracking vehicle after the first time
    else:
        # Loop current vehicle list
        for trk_id, dist, bb, cf, cl in zip(tracker_id, distance, boxes, confs, clss):
            trk_id_match_flg = False
            # Loop old vehicle list
            for idx,ele in enumerate(tracker_change_lane):
                # If current vehicle match old vehicle (that mean same vehicle)
                if trk_id == ele['tracker_id']:
                    trk_id_match_flg = True
                    
                    # If distance between center of vehicle bounding box and center of lane < 5 pixel,
                    # we will not track that vehicle.
                    if dist < 5:
                        ele['inside_lane_flg'] = True
                    
                    # Remove vehicle which inside lane from old vehicle and start checking another vehicle
                    if ele['inside_lane_flg'] == True:
                        tracker_change_lane.pop(idx)
                        break
                        
                    # If vehicle getting closer to the lane, we will increase counter changing lane.
                    if dist < ele['distance']:
                        ele['change_lane_counter'] += 1
                    # If not, we will increase counter no changing lane.
                    else:
                        ele['no_change_lane_counter'] += 1
                    
                    # Use average distance everytime to make it stable
                    ele['distance'] = (ele['distance'] + dist)/2
                    
                    # If vehicle not changing lane
                    if ele['change_lane_flg'] is False:
                        # And chaning lane counter >= 10,
                        # reset no changing lane counter and set flag changing lane for vehicle
                        if ele['change_lane_counter'] >= 10:
                            ele['no_change_lane_counter'] = 0
                            ele['change_lane_flg'] = True
                    # If vehicle changing lane
                    else:
                        # And no chaning lane counter >= 10,
                        # reset changing lane counter and set flag no changing lane for vehicle
                        if ele['no_change_lane_counter'] >= 10:
                            ele['change_lane_counter'] = 0
                            ele['change_lane_flg'] = False
                    
                    # Store frame number exist this vehicle
                    ele['frame_exist_vehicle'] = frame_count
                    
                    # Store bounding box, confidence, class when detect vehicle
                    ele['boxes'] = bb
                    ele['confs'] = cf
                    ele['clss'] = cl
                    
                    break
                else:
                    pass
            
            # If current vehicle not match any old vehicle, add that current vehicle to old vehicle list
            if trk_id_match_flg is False:
                temp_dict = dict()
                temp_dict['tracker_id'] = trk_id
                temp_dict['distance'] = dist
                temp_dict['change_lane_counter'] = 0
                temp_dict['no_change_lane_counter'] = 0
                temp_dict['frame_exist_vehicle'] = frame_count
                temp_dict['change_lane_flg'] = False
                temp_dict['inside_lane_flg'] = False
                temp_dict['boxes'] = bb
                temp_dict['confs'] = cf
                temp_dict['clss'] = cl
                tracker_change_lane.append(temp_dict)
    
    # If any old vehicle not exist in current frame, remove that old vehicle from old vehicle list
    for idx,ele in enumerate(tracker_change_lane):
        if ele['frame_exist_vehicle'] != frame_count:
            tracker_change_lane.pop(idx)
        else:
            pass
    
    return tracker_change_lane
