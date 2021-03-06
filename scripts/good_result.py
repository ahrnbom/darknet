from glob import glob
import cv2
import os
import sys
from folder import mkdir

basepath = '/media/ma/48026b8d-78d7-48d8-90ec-0ab2252ab34d/ma/miotcd/MIO-TCD-Localization/train/'
fold = sys.argv[1]
print("Using fold {}".format(fold))

foldername = "goodresults_{}".format(fold)
mkdir(foldername)

orig = glob("results/{}*.txt".format(fold))
miotcd_classes = ["articulatedtruck", "bicycle", "bus", "car", "motorcycle", "motorizedvehicle", "nonmotorizedvehicle", "pedestrian", "pickuptruck", "singleunittruck", "workvan"]

old = glob("{}/*.txt".format(foldername))
for o in old:
    os.remove(o)
    print("Removed {}".format(o))

for o in orig:
    splot = o.strip(".txt").split("_")
    cname = '_'.join(splot[1:])
    
    if cname in miotcd_classes:
        print(cname)
        
        with open(o,'r') as f:
            lines = [line.rstrip('\n') for line in f]    
            
        for line in lines:
            splot = line.split(" ")
            if len(splot) == 6:
                if len(splot[0]):
                    imname = splot[0]
                    can_imname = imname
                else:
                    imnum = int(can_imname)+1
                    new_imname = str(imnum)
                    while len(new_imname) < len(can_imname):
                        new_imname = "0" + new_imname
                    imname = new_imname    
                conf = float(splot[1])
                x1 = float(splot[2])
                y1 = float(splot[3])
                x2 = float(splot[4])
                y2 = float(splot[5])
            else:
                print("What is this I don't even")
                print(splot)
            
            if conf > 0.1:
                xc = (x1 + x2)/2
                yc = (y1 + y2)/2
                bw = x2 - x1
                bh = y2 - y1
                
                #if bw > 0:
                impath = basepath + imname + '.jpg'
                #im = cv2.imread(impath)
                #print(impath)
                #shaep = im.shape
                shaep = [480,720]
                xc /= shaep[1]
                yc /= shaep[0]
                bw /= shaep[1]
                bh /= shaep[0]
                newline = "{} {} {} {} {} {}\n".format(cname, conf, xc, yc, bw, bh)
                
                with open("{}/{}.txt".format(foldername, imname),'a') as of:
                    of.write(newline)
       
        
        miotcd_classes.remove(cname)
print(miotcd_classes)
