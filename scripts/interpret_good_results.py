from glob import glob
import cv2
from random import shuffle
import numpy as np
import sys
sys.path.append("../ensemble-objdet/")
from ensemble import GeneralEnsemble

conf_thresh = 0.2
ndets = 2

miotcd_classes = ["articulatedtruck", "bicycle", "bus", "car", "motorcycle", "motorizedvehicle", "nonmotorizedvehicle", "pedestrian", "pickuptruck", "singleunittruck", "workvan"]
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
ress = glob('goodresults1/*.txt')
shuffle(ress)

respath = ress[0]
respaths = []
for i in range(1,ndets+1):
    respaths.append(respath.replace("goodresults1/", "goodresults{}/".format(i)))

name = respath.split('/')[-1].strip('.txt')
impath = basepath + name + '.jpg'
im = cv2.imread(impath)

lines = []
for i in range(0, ndets):
    print(respaths[i])
    with open(respaths[i], 'r') as f:
        lines_tmp = [line.rstrip('\n') for line in f]   
        lines.append(lines_tmp)
    
w = im.shape[1]
h = im.shape[0]

ims = []
dets = []
for iline in range(0, ndets):
    det = []

    lines_ = lines[iline]
    im2show = im.copy()
    for line in lines_:
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
            box = [xc, yc, bw, bh, cnum, conf]
            det.append(box)
            
            cv2.rectangle(im2show, (x1, y1), (x2, y2), class_colors[cnum], 2)
            
            text = cname + " " + ('%.2f' % conf)
            tlen = len(text)*7
            
            text_top = (x1, y1-15)
            text_bot = (x1 + tlen, y1)
            text_pos = (x1 + 5, y1-5)
            cv2.rectangle(im2show, text_top, text_bot, class_colors[cnum], -1)
            cv2.putText(im2show, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,0), 1)
    ims.append(im2show)
    dets.append(det)
    
ens = GeneralEnsemble(dets)
im2show = im.copy()
for box in ens:
    xc = box[0]
    yc = box[1]
    bw = box[2]    
    bh = box[3]
    cnum = box[4]
    conf = box[5]
    
    x1 = int(xc - bw/2)
    x2 = int(xc + bw/2)
    y1 = int(yc - bh/2)
    y2 = int(yc + bh/2)
    
    cname = miotcd_classes[cnum]
    
    cv2.rectangle(im2show, (x1, y1), (x2, y2), class_colors[cnum], 2)
            
    text = cname + " " + ('%.2f' % conf)
    tlen = len(text)*7
    
    text_top = (x1, y1-15)
    text_bot = (x1 + tlen, y1)
    text_pos = (x1 + 5, y1-5)
    cv2.rectangle(im2show, text_top, text_bot, class_colors[cnum], -1)
    cv2.putText(im2show, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,0), 1)

#for i in range(0, ndets):            
#    cv2.imshow(name + " " + str(i+1), ims[i])    
#cv2.imshow(name + " ensemble", im2show)

bigim = np.zeros((h*2, w*ndets, 3), dtype=im2show.dtype)
for i in range(0, ndets):
    bigim[0:h, i*w:(i+1)*w, :] = ims[i]
cen = w*ndets/2    
bigim[h:2*h, cen-w/2:cen+w/2, :] = im2show
cv2.imshow(name, bigim)
cv2.waitKey(0)

