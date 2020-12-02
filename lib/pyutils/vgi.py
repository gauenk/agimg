
# -- python imports --
import numpy as np

def vgi_vari(img):
    r,g,b = 0,1,2
    num = img[:,:,g] - img[:,:,r]
    den = img[:,:,g] + img[:,:,r] - img[:,:,b]
    result = num / den
    result[result == np.inf] = 0
    return result

def vgi_tgi(img):
    r,g,b = 0,1,2
    return img[:,:,g] - 0.39 * img[:,:,r] - 0.61 * img[:,:,b]

