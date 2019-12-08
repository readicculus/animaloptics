# Source: https://dog-vision.andraspeter.com/technical.php
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import simulator.translations as trans

bgr = cv2.imread('samples/flower.jpg')

gamma_expand = 2.2
gamma_compressed = 1.0 / gamma_expand

im = bgr.astype('float') / 255.0
im = im ** gamma_expand
a = im.astype(np.float)*255
cv2.imwrite("figs/step1-gammaexpand.jpg", a)

b_human, g_human, r_human = cv2.split(im)

r_dog = np.add(r_human, g_human) * .5
g_dog = r_dog
b_dog = b_human
a = cv2.merge([b_dog, g_dog, r_dog]).astype(np.float)*255
cv2.imwrite("figs/step2-colorcorrect.jpg", a)
####   brightness discrimination
# https://jov.arvojournals.org/article.aspx?articleid=2121581
# humans are trichomat and our vision is most sensetive to green
# which these coefficients reflect
mean_brightness = np.mean(r_human) * .3 + \
                  np.mean(g_human) * .59 + \
                  np.mean(b_human) * .11
# human weber fraction = .11
# dog weber fraction ~.22
r_dog = (r_dog + mean_brightness) / 2.
g_dog = (g_dog + mean_brightness) / 2.
b_dog = (b_dog + mean_brightness) / 2.
im = cv2.merge([b_dog, g_dog, r_dog])
a = im.astype(np.float)*255
cv2.imwrite("figs/step3-brightnesscorrect.jpg", a)

# Visual Acuity
# The maximum visual acuity of the human eye is around 50 CPD[7] and 60 CPD[8].
# The measurements of dogs' visual acuity vary around 7.5-9 CPD[9] and 11.6 CPD[10].
# humans 20/20 dogs 20/75
im = trans.acuity_transform2d(im, 50, 10)
a = im.astype(np.float)*255
cv2.imwrite("figs/step4-visualacuity.jpg", a)
im = im ** gamma_compressed
a = im.astype(np.float)*255
cv2.imwrite("figs/step5-gammacompress.jpg", a)

