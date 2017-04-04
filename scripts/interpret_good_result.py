from glob import glob
import cv2
from random import shuffle
import numpy as np

conf_thresh = 0.2

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

basepath = '/media/ma/48026b8d-78d7-48d8-90ec-0ab2252ab34d/ma/miotcd/MIO-TCD-Localization/train/'
ress = glob('goodresults/*.txt')
shuffle(ress)

respath = ress[0]

name = respath.split('/')[-1].strip('.txt')
impath = basepath + name + '.jpg'
im = cv2.imread(impath)

lines = []
try:
    with open(respath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]   
except:
    pass
    
w = im.shape[1]
h = im.shape[0]

im2show = im.copy()
for line in lines:
    splot = line.split(" ")
    cname = splot[0]
    conf = float(splot[1])
    xc = w*float(splot[2])
    yc = h*float(splot[3])
    bw = w*float(splot[4])
    bh = h*float(splot[5])
    
    if conf > conf_thresh:
        cnum = miotcd_classes.index(cname)
        x1 = int(xc - bw/2)
        x2 = int(xc + bw/2)
        y1 = int(yc - bh/2)
        y2 = int(yc + bh/2)
        
        cv2.rectangle(im2show, (x1, y1), (x2, y2), class_colors[cnum], 2)
        
        text = cname + " " + ('%.2f' % conf)
        tlen = len(text)*7
        
        text_top = (x1, y1-15)
        text_bot = (x1 + tlen, y1)
        text_pos = (x1 + 5, y1-5)
        cv2.rectangle(im2show, text_top, text_bot, class_colors[cnum], -1)
        cv2.putText(im2show, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,0), 1)
        
cv2.imshow(name, im2show)
cv2.waitKey(0)
