import cv2
import numpy as np

def window_1d(im, n):
    h,w = im.shape
    imout = np.copy(im)
    for i in range(n,w-n):
        for j in range(h):
            l = im[j,i-n]
            r = im[j,i+n]
            px = (float(l)+float(r))/2.0
            imout[j,i] = px
    return imout

def acuity_transform2d(img, acuity_src, acuity_dst):
    c = float(acuity_src)/float(acuity_dst)
    if c < 0.0:
        # acuity is actually higher for dst and we can't increase "resolution"
        return img
    factor = int(c/2)
    factor = min(factor, 20)

    chans =  cv2.split(img)
    cl = len(chans)
    for c in range(cl):
        for i in range(1,factor+1):
            chans[c] = window_1d(chans[c], i)  # horizontal pass
            chans[c] = window_1d(chans[c].T, i).T  # vertical pass


    out = cv2.merge(chans)

    return out

