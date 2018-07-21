=Installation on Ubuntu

==Prerequiments

GStreamer 1.0 (Use command 'sudo apt install gstreamer1.0')
python 3.6
pip3 util (can be installed with 'sudo apt install python3-pip')
virtualenv setuptools (can be installed with 'pip3 install virtualenv setuptools')

==Setup deveploment environment

"""
git clone [url]
cd streamsaver
virtualenv -p /usr/bin/python3 .pyenv
source .pyenv/bin/activate

pip3 install -r requirements.txt
python setup.py install
"""

After this command `transform` will become availible in PATH of virtual environment

== Run locally

== Build distribution

`python setup.py sdist`

to install package run

`pip install dist/streamsaver-1.0.2.tar.gz`

== Run unittests

`PYTHONPATH=./:$PYTHONPATH python3 -m unittest discover -s streamsaver/test`
