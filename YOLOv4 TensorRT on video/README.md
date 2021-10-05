# YOLOv4 TensorRT


**1. Set nvcc path:**
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
3. Install pycuda
```
pip3 install cython
pip3 install pycuda
```
5. Install onnx
```
pip3 install onnx=1.4.1
```
7. Make plugins
- Go to folder "plugins", run command below. When done, there will be files "libyolo_layer.so" and yolo_layer.o generated.
```
make
```
9. Dowload weight and cfg
```
./dowload.sh
```
11. YOLO to onnx
```
python3 yolo_to_onnx.py -m yolov4-416
```
13. onnx to trt
```
python3 onnx_to_tensorrt.py -m yolov4-416
```
15. run model
```
python3 trt_yolo.py --image traffic.mp4 -m yolov4-416
python3 trt_yolo.py --video traffic.mp4 -m yolov4-416
```
17. eval
