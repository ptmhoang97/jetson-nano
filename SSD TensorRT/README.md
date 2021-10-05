**1. Install pycuda**
```
pip3 install cython
pip3 install pycuda
```
**2. Upgrade graphsurgeon.py**
```
sudo sed -i '88 a \ \ \ \ node.attr["dtype"].type = 1' /usr/lib/python3.6/dist-packages/graphsurgeon/node_manipulation.py
```
**3. Install TensorFlow:**
```
sudo apt-get update
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
**5. Build engine**
- Go to folder "ssd":
```
./build_engines.sh
```
