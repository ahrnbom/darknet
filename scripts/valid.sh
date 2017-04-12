./darknet detector valid cfg/$1.data cfg/yolo-miotcd.cfg yolo-$2_final.weights 2>&1 | tee output_valid.log
