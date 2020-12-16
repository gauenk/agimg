
# -- python imports --
import numpy as np

# -- [local] project imports --
from .misc import np_divide_ignore

def compute_vgi(img,vgi_name):
    if vgi_name == "vari":
        return vgi_vari(img)
    elif vgi_name == "tgi":
        return vgi_tgi(img)
    else:
        raise KeyError("Unknown VGI [{vgi_name}]")

def vgi_vari(img):
    r,g,b = 0,1,2
    num = img[:,:,g] - img[:,:,r]
    den = img[:,:,g] + img[:,:,r] - img[:,:,b]
    result = np_divide_ignore(num,den)
    return result

def vgi_tgi(img):
    r,g,b = 0,1,2
    return img[:,:,g] - 0.39 * img[:,:,r] - 0.61 * img[:,:,b]

