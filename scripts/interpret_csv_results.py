import csv
import sys
from random import randint
import cv2
import numpy as np

fold = sys.argv[1]
tt = sys.argv[2]
chooseim = False
if len(sys.argv) > 3:
    imchoice = sys.argv[3]
    chooseim = True

conf_thresh = 0.2

if fold == "gt":
    csvpath = 'csv_results/gt_train.csv'
else:
    csvpath = 'csv_results/miotcd{}_{}.csv'.format(fold, tt)
with open(csvpath, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    rows = [r for r in reader]

nrows = len(rows)
i = randint(0, nrows-1)
somerow = rows[i]
imname = somerow[0]
if chooseim:
    imname = imchoice

found = []
for row in rows:
    if row[0] == imname:
        found.append(row)

basepath = '/media/ma/48026b8d-78d7-48d8-90ec-0ab2252ab34d/ma/miotcd/MIO-TCD-Localization/{}/'.format(tt)
impath = basepath + imname + '.jpg'
im = cv2.imread(impath)

miotcd_classes = ["articulated_truck", "bicycle", "bus", "car", "motorcycle", "motorized_vehicle", "non-motorized_vehicle", "pedestrian", "pickup_truck", "single_unit_truck", "work_van"]
num_classes = len(miotcd_classes)
class_colors = []
for i in range(0, num_classes):
    # This can probably be written in a more elegant manner
    hue = 255*i/num_classes
    col = np.zeros((1,1,3)).astype("uint8")
    col[0][0][0] = hue
    col[0][0][1] = 128 # Saturation
    col[0][0][2] = 255 # Value
    cvcol = cv2.cvtColor(col, cv2.COLOR_HSV2BGR)
    col = (int(cvcol[0][0][0]), int(cvcol[0][0][1]), int(cvcol[0][0][2]))
    class_colors.append(col) 
    
w = im.shape[1]
h = im.shape[0]

im2show = im.copy()
for row in found:
    if fold == "gt":
        cname = row[1]
        x1 = int(row[2])
        y1 = int(row[3])
        x2 = int(row[4])
        y2 = int(row[5])
        conf = 1.0
    else:
        cname = row[1]
        conf = float(row[2])
        x1 = int(row[3])
        y1 = int(row[4])
        x2 = int(row[5])
        y2 = int(row[6])
        
    if conf > conf_thresh:
        cnum = miotcd_classes.index(cname)

        cv2.rectangle(im2show, (x1, y1), (x2, y2), class_colors[cnum], 2)
        
        if fold == "gt":
            text = cname    
        else:
            text = cname + " " + ('%.2f' % conf)
        tlen = len(text)*7
        
        text_top = (x1, y1-15)
        text_bot = (x1 + tlen, y1)
        text_pos = (x1 + 5, y1-5)
        cv2.rectangle(im2show, text_top, text_bot, class_colors[cnum], -1)
        cv2.putText(im2show, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,0), 1)
        
cv2.imshow(imname, im2show)
cv2.imwrite("out.jpg", im2show)
cv2.waitKey(0)

