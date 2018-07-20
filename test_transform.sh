#!/bin/sh

#PYTHONPATH=./:$PYTHONPATH python3 streamsaver/main.py -u udp://localhost:6002 -o mp4 -d ./out.mp4 -n 3000
#PYTHONPATH=./:$PYTHONPATH python3 streamsaver/main.py -u tcp://localhost:5000 -o mp4 -d ./out2.mp4 -n 3000
PYTHONPATH=./:$PYTHONPATH python3 streamsaver/main.py -u rtsp://localhost:1235/file2.rtsp -o mp4 -d ./out2.mp4
#PYTHONPATH=./:$PYTHONPATH python3 streamsaver/main.py -u rtsp://localhost:1235/file.rtsp -o frame -d ./out%0d.jpg
#PYTHONPATH=./:$PYTHONPATH python3 streamsaver/main.py -u udp://localhost:6002 -o frame -d ./out%0d.jpg