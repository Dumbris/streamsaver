=Installation on Ubuntu

==Prerequiments

GStreamer lib
python 3.6
pip3 util (can be installed with 'apt-get install python3-pip')
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

== Run test

`python3 -m unittest`
