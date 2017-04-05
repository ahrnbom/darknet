./darknet detector iou cfg/$1.data cfg/yolo.2.0.miotcd.cfg backup/$2.weights 2>&1 | tee output_test_$1_$2.log
