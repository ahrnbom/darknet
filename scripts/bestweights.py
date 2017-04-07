import numpy as np
import matplotlib.pyplot as plt

a = np.arange(7623000,7723000,1000).tolist()
n =  len(a)
ious = np.zeros(n)
recas = np.zeros(n)

fold = "miotcd1"

for i in range(0,n):
    fname = "logs/output_test_{}_yolo_{}.log".format(fold, a[i])
    with open(fname, 'r') as f:
        lines = [line.strip('\n') for line in f.readlines()]
    lastline = lines[-1]
    splot = lastline.split(" ")
    iou = float(splot[-1])
    ious[i] = iou
    
    secondlast = lines[-2]
    splot = secondlast.split(":")
    recastr = splot[-1].strip("%")
    recas[i] = float(recastr)
    
best = np.argmax(ious)
abest = a[best]
print("Best IOU was {}".format(abest))

best2 = np.argmax(recas)
abest2 = a[best2]
print("Best recall was {}".format(abest2))
    
plt.plot(a, ious)
plt.plot(a, recas)
plt.xlabel("images processed")
plt.ylabel("average iou, recall (%)")
plt.title("{}, best was {}".format(fold, abest))
plt.grid(True)
plt.savefig("{}.png".format(fold))
plt.show()



