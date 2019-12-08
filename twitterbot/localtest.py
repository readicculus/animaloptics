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
im = cv2.imread('samples/image1.jpg')
im = cv2.imread('samples/bars.png')
sim = Simulator(simulator.dog, im)
sim2 = Simulator(simulator.bee, im)
sim3 = Simulator(simulator.cat, im)
rgb = sim.process()
showrgb(rgb)
rgb = sim2.process()
showrgb(rgb)
rgb = sim3.process()
showrgb(rgb)