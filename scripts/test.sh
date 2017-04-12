./darknet detector iou cfg/$1.data cfg/yolo-miotcd.cfg backup/$1/$2.weights 2>&1 | tee logs/output_test_$1_$2.log
