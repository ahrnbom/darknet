from glob import glob
import cv2
import os

basepath = '/media/ma/48026b8d-78d7-48d8-90ec-0ab2252ab34d/ma/miotcd/MIO-TCD-Localization/'

train = sorted(glob('{}{}/*.jpg'.format(basepath, 'train')))
test = sorted(glob('{}{}/*.jpg'.format(basepath, 'test')))

with open("../data/miotcd-train.txt",'w+') as f:
    for t in train:
        f.write(t + "\n")
        
with open("../data/miotcd-test.txt",'w+') as f:
    for t in test:
        f.write(t + "\n")        
        
# Convert ground truth to yolo format

# zero-based
yolo_classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

miotcd_classes = ["articulated_truck", "bicycle", "bus", "car", "motorcycle", "motorized_vehicle", "non_motorized_vehicle", "predestrian", "pickup_truck", "single_unit_truck", "work_van"]

class_conv = {"articulated_truck" : "boat",
              "bicycle": "bicycle",
              "bus": "bus",
              "car": "car",
              "motorcycle": "motorbike",
              "motorized_vehicle": "aeroplane",
              "non-motorized_vehicle": "horse",
              "pedestrian": "person",
              "pickup_truck": "train",
              "single_unit_truck": "chair",
              "work_van": "cow"}
              
with open('{}gt_train.csv'.format(basepath), 'r') as f:
    gt = [x.strip('\n') for x in f.readlines()]
    
# Remove any pre-existing .txt files in the test folder
test_txt = glob("{}train/*.txt".format(basepath))
for txt in test_txt:
    print("Deleted " + txt)
    os.remove(txt)
    
for line in gt:
    splot = line.split(',')
    fname = splot[0]
    class_name = splot[1]
    x1 = float(splot[2])
    y1 = float(splot[3])
    x2 = float(splot[4])
    y2 = float(splot[5])
    
    impath = "{}train/{}.jpg".format(basepath, fname)
    im = cv2.imread(impath)
    height, width, channels = im.shape
    
    xc = ((x1/width) + (x2/width))/2
    yc = ((y1/height) + (y2/height))/2
    bw = (x2/width) - (x1/width)
    bh = (y2/height) - (y1/height)
    
    yolo_class = class_conv[class_name]
    class_num = yolo_classes.index(yolo_class)
    
    newline = "{} {} {} {} {}\n".format(class_num, xc, yc, bw, bh)
    fpath = "{}train/{}.txt".format(basepath, fname)
    with open(fpath, 'a') as f:
        f.write(newline)
    print("Written " + fname)
