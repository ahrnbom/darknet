from glob import glob
import sys

target = sys.argv[1]

all_src = glob('src/*.c')

for src in all_src:
    with open(src, 'r') as f:
        for line in f.readlines():
            if target in line:
                print(src)
                print(line)
