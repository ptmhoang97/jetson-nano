# YOLOv4 object detection on video
**Prerequisites:**
- Install YOLOv4 on Jetson Nano, follow [this](https://github.com/ptmhoang97/jetson/tree/main/YOLOv4%20installation).

**1. Setup for "main_video.py":**
- Copy "main_video.py" in this repo to darknet folder.
- Change path if necessary:\
```
configPath = "./cfg/yolov4-tiny.cfg" 
weightPath = "./yolov4-tiny.weights" 
metaPath = "./cfg/coco.data"
videoPath = "./traffic.mp4"
```

**2. Run model:**
- Open terminal window at darknet folder and run command:\
`python3 main_video.py`
- It will show video window and save to a video file name "output_yolo.mp4":\
![image](https://user-images.githubusercontent.com/53186326/135756560-c5eb85ce-f2cb-480a-ad75-94ab4390ab0c.png)
