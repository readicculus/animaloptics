import cv2
import numpy as np
import simulator.translations as trans

def cat(bgr):
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    gamma_expand = 2.2
    gamma_compressed = 1.0/gamma_expand

    im = rgb.astype('float')/255.0
    im = im**gamma_expand

    r_human,g_human,b_human = cv2.split(im)

    r_cat = np.add(r_human, g_human)*.5
    g_cat = r_cat
    b_cat = b_human*.5

    ####   brightness discrimination
    # https://jov.arvojournals.org/article.aspx?articleid=2121581
    # humans are trichomat and our vision is most sensetive to green
    # which these coefficients reflect
    mean_brightness = np.mean(r_human)*.3 + \
                      np.mean(g_human) * .59 + \
                      np.mean(b_human) * .11
    # human weber fraction = .11
    # dog weber fraction ~.22
    r_cat = (r_cat+mean_brightness)/3.
    g_cat = (g_cat+mean_brightness)/3.
    b_cat = (b_cat+mean_brightness)/3.
    im = cv2.merge([r_cat, g_cat, b_cat])


    # Visual Acuity
    # The maximum visual acuity of the human eye is around 50 CPD[7] and 60 CPD[8].
    # The measurements of dogs' visual acuity vary around 7.5-9 CPD[9] and 11.6 CPD[10].
    #humans 20/20 dogs 20/75
    im = trans.acuity_transform(im, 60, 10)
    im = im**gamma_compressed


    return im