1. Install pycuda
2. Upgrade graphsurgeon.py
```
sudo sed -i '88 a \ \ \ \ node.attr["dtype"].type = 1' /usr/lib/python3.6/dist-packages/graphsurgeon/node_manipulation.py
```
2. Build engine
