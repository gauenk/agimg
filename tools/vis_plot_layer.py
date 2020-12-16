# -- python imports --
from PIL import Image
from pathlib import Path
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto

# -- project imports --
import _init_paths
from pyutils.vgi import compute_vgi
from pyutils.misc import get_xyz

def main():

    # -- plot layouts --
    root = Path("./data/plot_layer/")
    fn = Path("Simpson_plots_2019.shp")
    path = root / fn
    data = gpd.read_file(path)
    data.plot()
    plt.savefig("./layout.png",transparent=True,dpi=300,bbox_inches='tight')
    plt.close("all")

    # -- compute Vegetative Indices --
    img_path = "./data/NEPAC_L4_170801_200ft/DJI_1930.JPG"
    gps_coord = gpsphoto.getGPSData(img_path)
    raw_img = np.array(Image.open(img_path))

    vari_img = compute_vgi(raw_img,"vari")
    vari_img = normalize_img(vari_img)
    fig,ax = plt.subplots(figsize=(10,10))
    ax.imshow(vari_img,interpolation='none')
    plt.savefig("./vgi_vari.png",transparent=True,bbox_inches='tight',dpi=300)
    plt.close("all")

    tgi_img = compute_vgi(raw_img,"tgi")
    fig,ax = plt.subplots(figsize=(10,10))
    ax.imshow(tgi_img,interpolation='none')
    plt.savefig("./vgi_tgi.png",transparent=True,bbox_inches='tight',dpi=300)
    plt.close("all")

def normalize_img(img):
    img -= img.min()
    img /= img.max()
    return img


if __name__ == "__main__":
    main()
