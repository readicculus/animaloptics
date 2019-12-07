import cv2
import numpy as np
from matplotlib import pyplot as plt

def showgray(im):
    plt.imshow(im, cmap='gray',vmin=0, vmax=1)
    plt.show()
def showrgb(im):
    plt.imshow(im, vmin=0, vmax=1)
    plt.show()
import numpy as np
from numpy.lib.stride_tricks import as_strided


def strided_convolution(image, weight, stride):
    im_h, im_w = image.shape
    f_h, f_w = weight.shape

    out_shape = (1 + (im_h - f_h) // stride, 1 + (im_w - f_w) // stride, f_h, f_w)
    out_strides = (image.strides[0] * stride, image.strides[1] * stride, image.strides[0], image.strides[1])
    windows = as_strided(image, shape=out_shape, strides=out_strides)

    return np.tensordot(windows, weight, axes=((2, 3), (0, 1)))
def getkern(side):
    if side%2 == 0:
        side +=1
    kernel = np.zeros((side,side))
    mid = int((side+0.0)/2.0)
    kernel[mid][0] = 1
    kernel[mid][side-1] = 1
    kernel[0][mid] = 1
    kernel[side-1][mid] = 1
    kernel = kernel * (1 / 4)
    return kernel

# https://www.biorxiv.org/content/10.1101/328443v1.full
# https://www.good-lite.com/cw3/Assets/documents/ContrastSensitivity.pdf
def acuity_transform(img, acuity_src, acuity_dst):
    c = float(acuity_src)/float(acuity_dst)
    if c < 0.0:
        # acuity is actually higher for dst and we can't increase "resolution"
        return img
    factor = int(c/2)
    factor = min(factor, 20)


    # r, g, b = cv2.split(img)
    rn,gn,bn = cv2.split(img)
    for i in range(factor):
        #3,5,9
        kernel = getkern(i*2+3)
        rn = cv2.filter2D(rn, -1, kernel)
        gn = cv2.filter2D(gn, -1, kernel)
        bn = cv2.filter2D(bn, -1, kernel)


    out = cv2.merge([rn,gn,bn])

    return out
