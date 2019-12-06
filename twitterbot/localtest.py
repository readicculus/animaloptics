import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter

import simulator
from simulator.Simulator import Simulator

im = cv2.imread('../image1.jpg')
sim = Simulator(simulator.dog, im)
res = sim.process()
x=1