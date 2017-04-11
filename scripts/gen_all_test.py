import numpy as np
a = np.arange(500400,503300,200).tolist()

with open('scripts/all_test.sh', 'w+') as f:
    for i in range(0,5):
        for j in a:
            f.write("./scripts/test.sh miotcd{} yolo_{}\n".format(i+1,j))
