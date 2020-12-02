# -- python imports --
from PIL import Image
from pathlib import Path
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

def main():

    # -- plot layouts --
    root = Path("./data/plot_layer/")
    fn = Path("Simpson_plots_2019.shp")
    path = root / fn
    data = gpd.read_file(path)
    print(data)
    data.plot()
    plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    plt.close("all")

    # -- compute Vegetative Indices --
    img_path = "./data/NEPAC_L4_170801_200ft/DJI_1930.JPG"
    raw_img = np.array(Image.open(img_path))

    vari_img = vgi(raw_img,"vari")
    vari_img = normalize_img(vari_img)
    fig,ax = plt.subplots(figsize=(10,10))
    ax.imshow(vari_img,interpolation='none')
    plt.savefig("./vgi_vari.png",transparent=True,bbox_inches='tight',dpi=300)
    plt.close("all")

    tgi_img = vgi(raw_img,"tgi")
    fig,ax = plt.subplots(figsize=(10,10))
    ax.imshow(tgi_img,interpolation='none')
    plt.savefig("./vgi_tgi.png",transparent=True,bbox_inches='tight',dpi=300)
    plt.close("all")

    # -- sampling area layer --
    # arcgis; width of box or pixels within each box? a new raster. 

def normalize_img(img):
    img -= img.min()
    img /= img.max()
    return img

def vgi(img,vgi_name):
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
    result = num / den
    result[result == np.inf] = 0
    return result

def vgi_tgi(img):
    r,g,b = 0,1,2
    return img[:,:,g] - 0.39 * img[:,:,r] - 0.61 * img[:,:,b]

if __name__ == "__main__":
    main()
