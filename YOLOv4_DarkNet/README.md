# Install YOLOv4 on Jetson Nano

**1. Clone lastest darknet code:**
```
git clone https://github.com/AlexeyAB/darknet.git
cd darknet
```
**2. Modify "Makefile":**
```
GPU=1
CUDNN=1
CUDNN_HALF=1
OPENCV=1
AVX=0
OPENMP=1
LIBSO=1
ZED_CAMERA=0
ZED_CAMERA_v2_8=0

......

USE_CPP=0
DEBUG=0

ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]
```

**3. Set nvcc path:**
```
sudo gedit ~/.bashrc
```
```
# Add these lines at the end of file.
export PATH=${PATH}:/usr/local/cuda/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda/lib64
```
```
source ~/.bashrc
nvcc --version
```

**4. Build code:**
```
make
```
   - There will be file name "darknet" after finish.

**5. Set Jetson Nano to maximum performance:**
```
sudo nvpmodel -m 0
sudo jetson_clocks
```

**6. Dowload video on youtube:**
```
sudo -H pip3 install --upgrade youtube-dl
youtube-dl -F https://youtu.be/NcaGFp76BTY
```
- It will show of list format, I choose format 134:\
![image](https://user-images.githubusercontent.com/53186326/135750244-1d18a6fc-6fd2-49ad-ac52-ef63dd5f5245.png)
```
youtube-dl -f 134 https://youtu.be/NcaGFp76BTY
mv "Road traffic video for object recognition-NcaGFp76BTY.mp4" "traffic.mp4"
```

**7. Run model with executable file:**
   - Yolov4:
      - Preparation:
      ```
      # Download weight:
      wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4.weights -q --show-progress --no-clobber

      # Create yolov4-416.cfg with width=416, height=416 from yolov4.cfg:
      cat cfg/yolov4.cfg | sed -e '7s/width=608/width=416/' | sed -e '8s/height=608/height=416/' > cfg/yolov4-416.cfg
      ```
      - Test on image:
      ``` 
      ./darknet detector test cfg/coco.data cfg/yolov4-416.cfg yolov4.weights data/dog.jpg -gpus 0
      ```
      - Test on video:
      ```
      ./darknet detector demo cfg/coco.data cfg/yolov4-416.cfg yolov4.weights traffic.mp4 -gpus 0
      ```
   
   - Yolov4-tiny:
      - Preparation:
      ```
      # Download weight:
      wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights -q --show-progress --no-clobber
      ```
      - Test on image:
      ``` 
      ./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights data/dog.jpg -gpus 0
      ```
      - Test on video:
      ```
      ./darknet detector demo cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights traffic.mp4 -gpus 0
      ```
**7. Run model with python file:**
   - Ima
