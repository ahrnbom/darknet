stdbuf -o 0 nice -10 ./darknet detector train cfg/miotcd.data cfg/yolo.2.0.miotcd.cfg yolo.weights 2>&1 | tee output.log
