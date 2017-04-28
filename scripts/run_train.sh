make
stdbuf -o 0 nice -10 ./darknet detector train cfg/miotcd1.data cfg/yolo-miotcd.cfg imagenet.weights 2>&1 | tee output1.log
stdbuf -o 0 nice -10 ./darknet detector train cfg/miotcd2.data cfg/yolo-miotcd.cfg imagenet.weights 2>&1 | tee output2.log
stdbuf -o 0 nice -10 ./darknet detector train cfg/miotcd3.data cfg/yolo-miotcd.cfg imagenet.weights 2>&1 | tee output3.log
stdbuf -o 0 nice -10 ./darknet detector train cfg/miotcd4.data cfg/yolo-miotcd.cfg imagenet.weights 2>&1 | tee output4.log
stdbuf -o 0 nice -10 ./darknet detector train cfg/miotcd5.data cfg/yolo-miotcd.cfg imagenet.weights 2>&1 | tee output5.log
