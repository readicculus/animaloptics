import cv2
import numpy as np

im = np.zeros((30,1040)).astype(np.int8)
factor = 0
color = 1
idx = 0
for i in range(10):
    factor += 2
    print(factor)
    # r = 200
    # if (r/factor/2) % 2 != 1:
    #     r += factor*2
    r=100
    if i == 0 or i == 9:
        r = 120
    for j in range(0, r, factor):
        im[:,idx:idx+factor] = color
        color = (not color)
        idx += factor

im = im.astype(np.float)*255
cv2.imwrite('figs/bar.jpg', im)
x=1