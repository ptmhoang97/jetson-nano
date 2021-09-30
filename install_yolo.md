# Install Yolo on Jetson Nano

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
**3. Build code:**
```
make
```
   - There will be file name "darknet" after finish.

**4. Set Jetson Nano to maximum performance:**
```
sudo nvpmodel -m 0
sudo jetson_clocks
```
**5. Test with yolov4:**
   - Preparation:
   ```
   # Download weight:
   wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4.weights -q --show-progress --no-clobber
   
   # Create yolov4-416.cfg with width=416, height=416 from yolov4.cfg:
   cat cfg/yolov4.cfg | sed -e '7s/width=608/width=416/' | sed -e '8s/height=608/height=416/' > cfg/yolov4-416.cfg
   ```
   - Test on image:
   ``` 
   # Detect on image
   ./darknet detector test cfg/coco.data cfg/yolov4-416.cfg yolov4.weights data/dog.jpg -gpus 0
   ```
   - Test on video:
   ```
   ./darknet detector demo cfg/coco.data cfg/yolov4-416.cfg yolov4.weights traffic.mp4 -gpus 0
   ```
