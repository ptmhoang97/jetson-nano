# YOLOv4 object detection on image
**Prerequisites:**
- Install YOLOv4 on Jetson Nano, follow [this](https://github.com/ptmhoang97/jetson/tree/main/YOLOv4%20installation).

**1. Setup for "main_image.py":**
- Copy "main_image.py" in this repo to darknet folder.
- Change path in "main_image.py" if necessary:\
```
configPath = "./cfg/yolov4-tiny.cfg"
weightPath = "./yolov4-tiny.weights"
metaPath = "./cfg/coco.data"
imagePath = "./data/dog.jpg"
```

**2. Run model:**
- Open terminal window at darknet folder and run command:\
`python3 main_image.py`
- It will show image window and save to a image file name "output_yolo.jpg":\
![image](https://user-images.githubusercontent.com/53186326/135757366-8a571775-ab92-41ef-987c-caa51ce78d17.png)
