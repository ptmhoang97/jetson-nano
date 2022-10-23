# YOLOv4 TensorRT

Hint: Start from "Make plugins" below if you re-clone new repo (Make sure you already finished 0_Setup_Jetson_Nano before).

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
**Install pycuda**
```
pip3 install cython
pip3 install pycuda
```
**Install onnx**
```
sudo apt-get install libprotobuf-dev protobuf-compiler
pip3 install onnx==1.4.1
```
**Make plugins**
- Go to folder "plugins", open cmd window and run command below. When done, there will be files "libyolo_layer.so" and yolo_layer.o generated.
```
make
```
**Dowload weight and cfg**
- Go to folder "yolo", open cmd window and run command below:
```
chmod u+x dowload.sh
./dowload.sh
```
**YOLO to ONNX**
- Stay in cmd window of folder "yolo" and run command below:
```
python3 yolo_to_onnx.py -m yolov4-tiny-416
```
**ONNX to TensorRT**
- Stay in cmd window of folder "yolo" and run command below:
```
python3 onnx_to_tensorrt.py -m yolov4-tiny-416
```
**Run model**
- Go folder "YOLOv4_TensorRT", open cmd window and run command below:
```
python3 trt_yolo.py --image dog.jpg -m yolov4-tiny-416
python3 trt_yolo.py --video video1.mp4 -m yolov4-tiny-416
```
**Eval model with COCO**
```
wget http://images.cocodataset.org/zips/val2017.zip
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip val2017.zip
unzip annotations_trainval2017.zip
```
```
sudo pip3 install pycocotools
sudo pip3 install progressbar2
```
```
python3 eval_yolo.py -m yolov4-tiny-416
```
**Note**
- You can change "yolov4-tiny-416" to another model. Here is list of model:
```
yolov4
yolov4-288
yolov4-416
yolov4-tiny
yolov4-tiny-288
yolov4-tiny-416
```
