from glob import glob
import cv2
import os

basepath = '/media/ma/48026b8d-78d7-48d8-90ec-0ab2252ab34d/ma/miotcd/MIO-TCD-Localization/'

train = sorted(glob('{}{}/*.jpg'.format(basepath, 'train')))
test = sorted(glob('{}{}/*.jpg'.format(basepath, 'test')))

if False:
    with open("../data/miotcd-train.txt",'w+') as f:
        for t in train:
            f.write(t + "\n")
            
    with open("../data/miotcd-test.txt",'w+') as f:
        for t in test:
            f.write(t + "\n")        
        
# Convert ground truth to yolo format

# zero-based
yolo_classes = ["person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket","bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","couch","potted plant","bed","dining table","toilet","tv","laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"]

miotcd_classes = ["articulated_truck", "bicycle", "bus", "car", "motorcycle", "motorized_vehicle", "non_motorized_vehicle", "predestrian", "pickup_truck", "single_unit_truck", "work_van"]

class_conv = {"pedestrian": "person",
              "bicycle": "bicycle",
              "car": "car",
              "motorcycle": "motorcycle",
              "pickuptruck": "airplane",
              "bus": "bus",
              "motorizedvehicle": "train",
              "articulatedtruck": "boat",
              "workvan": "bench",
              "nonmotorizedvehicle": "horse",
              "singleunittruck": "truck"}

class_conv2 = {"person": "pedestrian",
"bicycle": "bicycle",
"car": "car",
"motorcycle": "motorcycle",
"airplane": "pickuptruck",
"bus": "bus",
"train": "motorizedvehicle",
"truck": "singleunittruck",
"boat": "articulatedtruck",
"traffic light": None,
"fire hydrant": None,
"stop sign": None,
"parking meter": None,
"bench": "workvan",
"bird": None,
"cat": None,
"dog": None,
"horse": "nonmotorizedvehicle",
"sheep": None,
"cow": None,
"elephant": None,
"bear": None,
"zebra": None,
"giraffe": None,
"backpack": None,
"umbrella": None,
"handbag": None,
"tie": None,
"suitcase": None,
"frisbee": None,
"skis": None,
"snowboard": None,
"sports ball": None,
"kite": None,
"baseball bat": None,
"baseball glove": None,
"skateboard": None,
"surfboard": None,
"tennis racket": None,
"bottle": None,
"wine glass": None,
"cup": None,
"fork": None,
"knife": None,
"spoon": None,
"bowl": None,
"banana": None,
"apple": None,
"sandwich": None,
"orange": None,
"broccoli": None,
"carrot": None,
"hot dog": None,
"pizza": None,
"donut": None,
"cake": None,
"chair": None,
"couch": None,
"potted plant": None,
"bed": None,
"dining table": None,
"toilet": None,
"tv": None,
"laptop": None,
"mouse": None,
"remote": None,
"keyboard": None,
"cell phone": None,
"microwave": None,
"oven": None,
"toaster": None,
"sink": None,
"refrigerator": None,
"book": None,
"clock": None,
"vase": None,
"scissors": None,
"teddy bear": None,
"hair drier": None,
"toothbrush": None}
              
with open('{}gt_train.csv'.format(basepath), 'r') as f:
    gt = [x.strip('\n') for x in f.readlines()]
    
# Remove any pre-existing .txt files in the test folder
test_txt = glob("{}train_txt/*.txt".format(basepath))
for txt in test_txt:
    print("Deleted " + txt)
    os.remove(txt)
    
for line in gt:
    splot = line.split(',')
    fname = splot[0]
    class_name = splot[1].replace('-','').replace('_','')
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
    fpath = "{}train_txt/{}.txt".format(basepath, fname)
    with open(fpath, 'a') as f:
        f.write(newline)
    print("Written " + fname)
