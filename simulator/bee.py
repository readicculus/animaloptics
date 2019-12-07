import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage.filters import gaussian_filter
import simulator.translations as trans

def bee(bgr):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    gamma_expand = 2.2
    gamma_compressed = 1.0/gamma_expand

    im = rgb.astype('float')/255.0
    im = im**gamma_expand

    r_human,g_human,b_human = cv2.split(im)

    r_bee = r_human
    r_bee[r_bee>.5] = .5
    g_bee = g_human
    b_bee = b_human

    ####   brightness discrimination
    # https://jov.arvojournals.org/article.aspx?articleid=2121581
    # humans are trichomat and our vision is most sensetive to green
    # which these coefficients reflect
    mean_brightness = np.mean(r_human)*.3 + \
                      np.mean(g_human) * .59 + \
                      np.mean(b_human) * .11
    # human weber fraction = .11
    # dog weber fraction ~.22
    r_bee = (r_bee+mean_brightness)/2.
    g_bee = (g_bee+mean_brightness)/2.
    b_bee = (b_bee+mean_brightness)/2.
    im = cv2.merge([r_bee, g_bee, b_bee])


    # Visual Acuity
    im = trans.acuity_transform(im, 60, 0.5)
    im = im**gamma_compressed


    return im
