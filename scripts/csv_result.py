from glob import glob
import cv2
import os
import sys
from folder import mkdir

comp = "browkin"

tt = sys.argv[2]
assert(tt == "train" or tt == "test")

if comp == "peano":
    basepath = '/media/ma/48026b8d-78d7-48d8-90ec-0ab2252ab34d/ma/miotcd/MIO-TCD-Localization/{}/'.format(tt)
elif comp == "browkin":
    basepath = '/home2/ahrnbom/MIO-TCD-Localization/{}/'.format(tt)
else:
    print("What is this I don't even")
    sys.exit()
    
fold = sys.argv[1]
print("Using fold {}".format(fold))

foldername = "csv_results"
mkdir(foldername)

outname = "{}/{}_{}.csv".format(foldername, fold, tt)
try:
    os.remove(outname)
    print("Removed old file")
except:
    print("Did not remove file")

orig = glob("results/miotcd*.txt")
miotcd_classes = ["articulatedtruck", "bicycle", "bus", "car", "motorcycle", "motorizedvehicle", "nonmotorizedvehicle", "pedestrian", "pickuptruck", "singleunittruck", "workvan"]

cnames2 = {"articulatedtruck": 'articulated_truck', 
           "bicycle": 'bicycle', 
           "bus": 'bus', 
           "car": 'car', 
           "motorcycle": 'motorcycle', 
           "motorizedvehicle": 'motorized_vehicle', 
           "nonmotorizedvehicle": 'non-motorized_vehicle', 
           "pedestrian": 'pedestrian', 
           "pickuptruck": 'pickup_truck', 
           "singleunittruck": 'single_unit_truck', 
           "workvan": 'work_van'}

all_lines = []
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
                shaep = [480,720]
                x1 /= shaep[1]
                y1 /= shaep[0]
                x2 /= shaep[1]
                y2 /= shaep[0]                
                                
                impath = basepath + imname + '.jpg'
                im = cv2.imread(impath)
                #print(impath)
                shaep2 = im.shape
                
                x1 *= shaep2[1]
                y1 *= shaep2[0]
                x2 *= shaep2[1]
                y2 *= shaep2[0]
                
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)
                
                cname2 = cnames2[cname]
                
                newline = "{},{},{},{},{},{},{}\n".format(imname, cname2, conf, x1, y1, x2, y2)
                
                all_lines.append(newline)
       
        
        miotcd_classes.remove(cname)
print(miotcd_classes)

def lolkey(line):
    return int(line.split(",")[0])

all_lines = sorted(all_lines, key=lolkey)
with open(outname, 'w') as f:
    for line in all_lines:
        f.write(line)
