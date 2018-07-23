#!/bin/sh

#gst-launch-1.0 -v v4l2src ! x264enc ! rtph264pay ! udpsink host=localhost port=6002
#gst-launch-1.0 -v filesrc location=e2e_tests/SampleVideo_1280x720_5mb.mp4 ! decodebin ! x264enc ! rtph264pay ! udpsink host=localhost port=6002
gst-launch-1.0 -v filesrc location=/media/data/snap/170928-cs224w-720.mp4 ! decodebin ! x264enc ! rtph264pay ! udpsink host=localhost port=6002
#gst-launch-1.0 -v filesrc location=/media/data/snap/170928-cs224w-720.mp4 ! decodebin ! x264enc ! rtph264pay ! tcpserversink host=0.0.0.0 port=5001

#gst-launch-1.0 -v filesrc location=/media/data/snap/170928-cs224w-720.mp4 ! decodebin ! x264enc ! rtph264pay ! rtspclientsink service=3000
#ffplay -rtsp_transport tcp -i rtsp://admin:admin@localhost:8080/0
