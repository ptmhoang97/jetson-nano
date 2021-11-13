# Install YOLOv4 on Jetson Nano

**Clone lastest darknet code:**
```
git clone https://github.com/AlexeyAB/darknet.git
cd darknet
```
**Modify "Makefile":**
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

**Set nvcc path:**
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

**Build code:**
```
make
```
   - There will be file name "darknet" after finish.

**Set Jetson Nano to maximum performance:**
```
sudo nvpmodel -m 0
sudo jetson_clocks
```

**Dowload video on youtube:**
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

**Dowload weight:**
```
./dowload.sh
```

**Run model with executable file:**
   - yolov4-416:
      - Test on image:
      ``` 
      ./darknet detector test cfg/coco.data yolov4-416.cfg yolov4.weights data/dog.jpg -gpus 0
      ```
      - Test on video:
      ```
      ./darknet detector demo cfg/coco.data yolov4-416.cfg yolov4.weights traffic.mp4 -gpus 0
      ```
   - yolov4-288:
      - Test on image:
      ``` 
      ./darknet detector test cfg/coco.data yolov4-288.cfg yolov4.weights data/dog.jpg -gpus 0
      ```
      - Test on video:
      ```
      ./darknet detector demo cfg/coco.data yolov4-288.cfg yolov4.weights traffic.mp4 -gpus 0
      ```
   - yolov4-tiny-416:
      - Test on image:
      ``` 
      ./darknet detector test cfg/coco.data yolov4-tiny-416.cfg yolov4-tiny.weights data/dog.jpg -gpus 0
      ```
      - Test on video:
      ```
      ./darknet detector demo cfg/coco.data yolov4-tiny-416.cfg yolov4-tiny.weights traffic.mp4 -gpus 0
      ```
   - yolov4-tiny-288:
      - Test on image:
      ``` 
      ./darknet detector test cfg/coco.data yolov4-tiny-288.cfg yolov4-tiny.weights data/dog.jpg -gpus 0
      ```
      - Test on video:
      ```
      ./darknet detector demo cfg/coco.data yolov4-tiny-288.cfg yolov4-tiny.weights traffic.mp4 -gpus 0
      ```
**Run model with python file:**
   - yolov4-416:
     - Test on image:
       - Change path in "main_image.py" if necessary:
       ```
       configPath = "./cfg/yolov4-416.cfg"
       weightPath = "./yolov4-416.weights"
       metaPath = "./cfg/coco.data"
       imagePath = "./data/dog.jpg"
       ```
       - Run model:
       ```
       python3 main_image.py
       ```
     - Test on video:
       - Change path in "main_video.py" if necessary:
       ```
       configPath = "./cfg/yolov4-416.cfg"
       weightPath = "./yolov4-416.weights"
       metaPath = "./cfg/coco.data"
       videoPath = "./traffic.mp4"
       ```
       - Run model:
       ```
       python3 main_video.py
       ```
   - yolov4-288:
     - Test on image:
       - Change path in "main_image.py" if necessary:
       ```
       configPath = "./cfg/yolov4-288.cfg"
       weightPath = "./yolov4-288.weights"
       metaPath = "./cfg/coco.data"
       imagePath = "./data/dog.jpg"
       ```
       - Run model:
       ```
       python3 main_image.py
       ```
     - Test on video:
       - Change path in "main_video.py" if necessary:
       ```
       configPath = "./cfg/yolov4-288.cfg"
       weightPath = "./yolov4-288.weights"
       metaPath = "./cfg/coco.data"
       videoPath = "./traffic.mp4"
       ```
       - Run model:
       ```
       python3 main_video.py
       ```
   - yolov4-tiny-416:
     - Test on image:
       - Change path in "main_image.py" if necessary:\
       ```
       configPath = "./cfg/yolov4-tiny-416.cfg"
       weightPath = "./yolov4-tiny-416.weights"
       metaPath = "./cfg/coco.data"
       imagePath = "./data/dog.jpg"
       ```
       - Run model:
       ```
       python3 main_image.py
       ```
     - Test on video:
       - Change path in "main_video.py" if necessary:
       ```
       configPath = "./cfg/yolov4-tiny-416.cfg"
       weightPath = "./yolov4-tiny-416.weights"
       metaPath = "./cfg/coco.data"
       videoPath = "./traffic.mp4"
       ```
       - Run model:
       ```
       python3 main_video.py
       ```
   - yolov4-tiny-288:
     - Test on image:
       - Change path in "main_image.py" if necessary:\
       ```
       configPath = "./cfg/yolov4-tiny-288.cfg"
       weightPath = "./yolov4-tiny-288.weights"
       metaPath = "./cfg/coco.data"
       imagePath = "./data/dog.jpg"
       ```
       - Run model:
       ```
       python3 main_image.py
       ```
     - Test on video:
       - Change path in "main_video.py" if necessary:
       ```
       configPath = "./cfg/yolov4-tiny-288.cfg"
       weightPath = "./yolov4-tiny-288.weights"
       metaPath = "./cfg/coco.data"
       videoPath = "./traffic.mp4"
       ```
       - Run model:
       ```
       python3 main_video.py
       ```
