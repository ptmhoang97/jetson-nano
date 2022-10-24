import math
from utils.lane_detection import get_x_y_bot_center_region_detect_lane

def prepare_input_for_display(img_copy,tracker_change_lane):
    tracker_elements_draw = []
    idx_inside_vehicle = []
    dis_inside_vehicle = []
    # Prepare input data for display function
    for idx,ele in enumerate(tracker_change_lane):
        temp = []
        trk_id = ele['tracker_id']
        boxes = ele['boxes']
        boxes[0] = int(boxes[0])
        boxes[1] = int(boxes[1])
        boxes[2] = int(boxes[2])
        boxes[3] = int(boxes[3])
        confs = ele['confs']
        clss = ele['clss']
        temp.append(trk_id)
        temp.append(boxes)
        temp.append(confs)
        temp.append(clss)
        temp.append(ele['change_lane_flg'])
        if ele['inside_lane_flg'] is True:
            region_x_bot_center_point,region_y_bot_center_point = \
                                    get_x_y_bot_center_region_detect_lane(img_copy)
                                    
            x_center_driver = region_x_bot_center_point
            y_center_driver = region_y_bot_center_point
            x_midpt_other_cars = int((boxes[0] + boxes[2])/2)
            y_midpt_other_cars = boxes[3]

            distance_pixel = int(math.sqrt((x_center_driver - x_midpt_other_cars)**2 + (y_center_driver - y_midpt_other_cars)**2))
            distance_real = (0.0039 * distance_pixel**2) - (0.1845 * distance_pixel) + 7.4355
            distance_real = round(distance_real,1)
            distance_real_loc = (int((x_center_driver + x_midpt_other_cars)/2),
                                 int((y_center_driver + y_midpt_other_cars)/2))
            temp.append(distance_real)
            temp.append(distance_real_loc)
            temp.append([x_center_driver,y_center_driver,x_midpt_other_cars,y_midpt_other_cars])
            idx_inside_vehicle.append(idx)
            dis_inside_vehicle.append(distance_real)
        else:
            temp.append(None)
            temp.append(None)
            temp.append(None)
        tracker_elements_draw.append(temp)
    
    # Display distance of only one vehicle which inside lane and closet to the driver
    if len(dis_inside_vehicle) != 0:
        min_distance = min(dis_inside_vehicle)
        temp_idx = dis_inside_vehicle.index(min_distance)
        idx_min_distance = idx_inside_vehicle[temp_idx]
        for idx,ele in enumerate(tracker_elements_draw):
            if idx != idx_min_distance:
                ele[5] = None
                ele[6] = None
                ele[7] = None

    return tracker_elements_draw
