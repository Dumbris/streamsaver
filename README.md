# Quickstart

This utility allows saving video streams into local files.

Install transform utility using a command
* `pip install dist/streamsaver-1.0.2.tar.gz`

Examples of usage:

Show help message
* `transform -h`

Save rtsp, udp or tcp stream into a local mp4 file.

* `transform -u udp://host:6002 -o mp4 -d ./out.mp4`
* `transform -u tcp://host:5000 -o mp4 -d ./out.mp4`
* `transform -u rtsp://host:1235/file2.rtsp -o mp4 -d ./out.mp4`

Save stream into series of jpg files.

* `transform -u rtsp://host:1235/file.rtsp -o frame -d ./out%0d.jpg`
* `transform -u udp://host:6002 -o frame -d ./out%0d.jpg`


## Requiments

* GStreamer 1.0 (Use command `sudo apt install gstreamer1.0`)
* python 3
* pip3 util (can be installed with `sudo apt install python3-pip`)

for development:
virtualenv setuptools (can be installed with `pip3 install virtualenv setuptools`)

## Using `streamsaver` as library

To call transform function from you python script you can import `streamsaver` and use streamsaver.pipeline.transform directly.
```python
from streamsaver.pipeline import transform

transform("udp://host:6002", "mp4", "/tmp/out.mp4")
```

Also, see `examples\appsink_example.py`. In this example, the numpy calculates the mean of pixels on a video stream.


## Setup development environment

```bash
git clone [url]
cd streamsaver
virtualenv -p /usr/bin/python3 .pyenv
source .pyenv/bin/activate
cd .pyenv/lib/python3.6/site-packages
ln -s /usr/lib/python3/dist-packages/gi
python setup.py install
```

After this command `transform` will become available in the PATH of the virtual environment

## Build distribution

`python setup.py sdist`

to install the built package run

`pip install dist/streamsaver-1.0.2.tar.gz`

## To run unittests

`PYTHONPATH=./:$PYTHONPATH python3 -m unittest discover -s streamsaver/test`

## To run e2e tests

Testing the video processing pipeline requires a source of a signal. Complex pipelines can be distributed on several hosts, and you need an orchestration tool to run tests.  So I am using robot framework for automatization. 

install requirements  
```bash
sudo pip3 install robotframework
sudo apt install ffmpeg
```

to run tests
```bash
cd e2e_tests
robot test_transform.robot
```
Than open report.html, log.html

