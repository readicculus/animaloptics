# Source: https://dog-vision.andraspeter.com/technical.php
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter

def showgray(im):
    plt.imshow(im, cmap='gray',vmin=0, vmax=1)
    plt.show()
def showrgb(im):
    plt.imshow(im, vmin=0, vmax=1)
    plt.show()

img = cv2.imread('image1.jpg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
r_human=img[:, :, 0].astype('float')/255.0
g_human=img[:, :, 1].astype('float')/255.0
b_human=img[:, :, 2].astype('float')/255.0

r_dog = np.add(r_human,g_human)*.5
g_dog = r_dog
b_dog = b_human

####   brightness discrimination
# https://jov.arvojournals.org/article.aspx?articleid=2121581
# humans are trichomat and our vision is most sensetive to green
# which these coefficients reflect
mean_brightness = np.mean(r_human)*.3 + \
                  np.mean(g_human) * .59 + \
                  np.mean(b_human) * .11
# human weber fraction = .11
# dog weber fraction ~.22
r_dog = (r_dog+mean_brightness)/2.
g_dog = (g_dog+mean_brightness)/2.
b_dog = (b_dog+mean_brightness)/2.
rgb = np.zeros(img.shape, 'float')
rgb[..., 0] = r_dog
rgb[..., 1] = g_dog
rgb[..., 2] = b_dog

# showgray(r_dog)
# showgray(g_dog)
# showgray(b_dog)

# Visual Acuity
# The maximum visual acuity of the human eye is around 50 CPD[7] and 60 CPD[8].
# The measurements of dogs' visual acuity vary around 7.5-9 CPD[9] and 11.6 CPD[10].
#humans 20/20 dogs 20/75
dog_sig = 3
r_dog = gaussian_filter(r_dog, sigma=dog_sig)
g_dog = gaussian_filter(g_dog, sigma=dog_sig)
b_dog = gaussian_filter(b_dog, sigma=dog_sig)
rgb[..., 0] = r_dog
rgb[..., 1] = g_dog
rgb[..., 2] = b_dog

showrgb(rgb)
showrgb(img)
