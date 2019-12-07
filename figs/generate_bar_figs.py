import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter

import simulator
from simulator.Simulator import Simulator
from simulator.translations import acuity_transform, acuity_transform2d, acuity_transform2d_bad


def showgray(im):
    plt.imshow(im, cmap='gray',vmin=0, vmax=1)
    plt.show()
def showrgb(im):
    plt.imshow(im, vmin=0, vmax=1)
    plt.show()
im = cv2.imread('samples/flower.jpg')
o = acuity_transform2d_bad(im, 20, 1)
cv2.imwrite("figs/flower_blur20x.jpg", o)


max=20
im = cv2.imread('samples/bar_orig.jpg', 0)
cv2.imwrite("figs/bar.jpg", im[:,max:1000-max])
big_im = None
big_im2 = None
for i in range(2,22,2):
    window = i
    o = acuity_transform2d_bad(im,i,1)
    o = o[:,max:1000-max]
    if big_im is None:
        big_im=o
    else:
        border = np.ones((5,o.shape[1]))*255
        big_im=np.vstack((big_im, border))
        big_im=np.vstack((big_im, o))
    # cv2.imwrite("figs/bar_bad_window%d.jpg"%window, o)

    o = acuity_transform2d(im,i,1)
    o = o[:,max:1000-max]
    if big_im2 is None:
        big_im2=o
    else:
        border = np.ones((5,o.shape[1]))*255
        big_im2=np.vstack((big_im2, border))
        big_im2=np.vstack((big_im2, o))
    # cv2.imwrite("figs/bar_window%d.jpg"%window, o)

cv2.imwrite("figs/barstacked_bad.jpg", big_im)
cv2.imwrite("figs/barstacked_good.jpg", big_im2)
