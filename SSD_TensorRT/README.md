
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
**Upgrade graphsurgeon.py**
```
sudo sed -i '88 a \ \ \ \ node.attr["dtype"].type = 1' /usr/lib/python3.6/dist-packages/graphsurgeon/node_manipulation.py
```
**Install TensorFlow:**
```
sudo apt-get update
```
```
sudo apt-get -y install libprotobuf-dev protobuf-compiler
```
```
sudo apt-get -y install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran
```
```
pip3 install -U pip testresources setuptools==49.6.0
```
```
pip3 install -U numpy==1.19.4 future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11 cython pkgconfig
```
```
pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v45 'tensorflow<2'
```
**Build engine**
- Go to folder "ssd":
```
sudo chmod +x build_engines.sh
./build_engines.sh
```

**Run model**
- Go to folder "SSD_TensorRT":
```
python3 trt_ssd.py --image dog.jpg --model ssd_mobilenet_v1_coco
python3 trt_ssd.py --video traffic.mp4 --model ssd_mobilenet_v1_coco
```
```
python3 trt_ssd_async.py --image dog.jpg --model ssd_mobilenet_v1_coco
python3 trt_ssd_async.py --video traffic.mp4 --model ssd_mobilenet_v1_coco
```

**Eval model**
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
python3 eval_ssd.py -m ssd_mobilenet_v1_coco
```
