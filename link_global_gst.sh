#!/bin/sh

cd .pyenv/lib/python3.6/site-packages
ln -s /usr/lib/python3/dist-packages/gi
exit 1
ln -s /usr/lib/python3.6/dist-packages/glib
ln -s /usr/lib/python3.6/dist-packages/gobject
ln -s /usr/lib/python3.6/dist-packages/gst-1.0
ln -s /usr/lib/python3.6/dist-packages/gstoption.so
ln -s /usr/lib/python3.6/dist-packages/pygst.pth
ln -s /usr/lib/python3.6/dist-packages/pygst.py