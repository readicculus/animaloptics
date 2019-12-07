import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter

import simulator
from simulator.Simulator import Simulator
from simulator.translations import acuity_transform, acuity_transform2d


def showgray(im):
    plt.imshow(im, cmap='gray',vmin=0, vmax=1)
    plt.show()
def showrgb(im):
    plt.imshow(im, vmin=0, vmax=1)
    plt.show()

def window_1d_bad(im, n):
    h,w = im.shape
    imout = np.copy(im)
    for i in range(n,w-n):
        for j in range(h):
            px = np.mean(im[j,i-n:i+n])
            imout[j,i] = px
    return imout

def acuity_transform2d_bad(img, acuity_src, acuity_dst):
    c = float(acuity_src)/float(acuity_dst)
    if c < 0.0:
        # acuity is actually higher for dst and we can't increase "resolution"
        return img
    factor = int(c/2)
    factor = min(factor, 20)


    # r, g, b = cv2.split(img)

    chans =  cv2.split(img)
    cl = len(chans)
    for c in range(cl):
        i = factor
        chans[c] = window_1d_bad(chans[c], factor)
        chans[c] = window_1d_bad(chans[c].T, i).T


    out = cv2.merge(chans)

    return out

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
