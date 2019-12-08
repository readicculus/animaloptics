import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter

import simulator
from simulator.Simulator import Simulator
def showgray(im):
    plt.imshow(im, cmap='gray',vmin=0, vmax=1)
    plt.show()
def showrgb(im):
    plt.imshow(im, vmin=0, vmax=1)
    plt.show()
im = cv2.imread('samples/flower.jpg')
rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
gamma_expand = 2.2
gamma_compressed = 1.0 / gamma_expand

im = rgb.astype('float') / 255.0
# im = im ** gamma_expand

r_human, g_human, b_human = cv2.split(im)

# r_dog = np.add(r_human, g_human) * .5
# g_dog = r_dog
# b_dog = b_human

r_dog = r_human
g_dog = g_human
b_dog = b_human
####   brightness discrimination
# https://jov.arvojournals.org/article.aspx?articleid=2121581
# humans are trichomat and our vision is most sensetive to green
# which these coefficients reflect
mean_brightness = np.mean(r_human) * .3 + \
                  np.mean(g_human) * .59 + \
                  np.mean(b_human) * .11
# human weber fraction = .11
# dog weber fraction ~.22
r_dog2 = (r_dog) / 2.
g_dog2 = (g_dog) / 2.
b_dog2 = (b_dog) / 2.
im2 = cv2.merge([b_dog2, g_dog2, r_dog2])

# im2 = im2 ** gamma_compressed
imx = cv2.merge([b_dog2, g_dog2, r_dog2])
imx[:,:,0] = 0
imx[:,:,1] = 0
cv2.imwrite("figs/r_human.jpg", imx.astype(np.float)*255)
imx = cv2.merge([b_dog2, g_dog2, r_dog2])
imx[:,:,0] = 0
imx[:,:,2] = 0
cv2.imwrite("figs/g_human.jpg", imx.astype(np.float)*255)
imx = cv2.merge([b_dog2, g_dog2, r_dog2])
imx[:,:,1] = 0
imx[:,:,2] = 0
cv2.imwrite("figs/b_human.jpg", imx.astype(np.float)*255)

r_dog3 = (r_dog + mean_brightness) / 2.
g_dog3 = (g_dog + mean_brightness) / 2.
b_dog3 = (b_dog + mean_brightness) / 2.
im3 = cv2.merge([b_dog3, g_dog3, r_dog3])
# im3 = im3 ** gamma_compressed

cv2.imwrite("figs/weberonly.jpg", im2.astype(np.float)*255)
cv2.imwrite("figs/weberwithmean.jpg", im3.astype(np.float)*255)
