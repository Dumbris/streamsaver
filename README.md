# Quick start

Install transform utility using command
`pip install dist/streamsaver-1.0.2.tar.gz`

Examples of usage:
Save rtsp, udp or tcp stream into localh mp4 file.

`transform -u udp://host:6002 -o mp4 -d ./out.mp4`
`transform -u tcp://host:5000 -o mp4 -d ./out.mp4`
`transform -u rtsp://host:1235/file2.rtsp -o mp4 -d ./out.mp4`

Save stream into series of jpg files.

`transform -u rtsp://host:1235/file.rtsp -o frame -d ./out%0d.jpg`
`transform -u udp://host:6002 -o frame -d ./out%0d.jpg`


## Prerequiments

GStreamer 1.0 (Use command 'sudo apt install gstreamer1.0')
python 3
pip3 util (can be installed with 'sudo apt install python3-pip')

for development:
virtualenv setuptools (can be installed with 'pip3 install virtualenv setuptools')

## Setup deveploment environment

```
git clone [url]
cd streamsaver
virtualenv -p /usr/bin/python3 .pyenv
source .pyenv/bin/activate
cd .pyenv/lib/python3.6/site-packages
ln -s /usr/lib/python3/dist-packages/gi
python setup.py install
```

After this command `transform` will become availible in the PATH of virtual environment

## Build distribution

`python setup.py sdist`

to install package run

`pip install dist/streamsaver-1.0.2.tar.gz`

## To run unittests

`PYTHONPATH=./:$PYTHONPATH python3 -m unittest discover -s streamsaver/test`

## To run e2e tests

End to end tests requiments  
```
sudo pip3 install robotframework
sudo apt install ffmpeg
```

to run tests
```
cd e2e_tests
robot test_transform.robot
```

