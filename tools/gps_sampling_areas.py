# -- python imports --
from PIL import Image
from pathlib import Path
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto

# -- project imports --
import _init_paths
from pyutils.vgi import *

def load_plot_layout(root):
    fn = Path("Simpson_plots_2019.{postfix}")
    path = root / fn
    plot_layout = gpd.read_file(path)
    # plot_layout.plot()
    # plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    # plt.close("all")
    return plot_layout    

def load_sampling_areas(root,postfix):
    fn = Path("Sampling_areas_test.{postfix}")
    path = root / fn
    sampling_areas = gpd.read_file(path)
    # plot_layout.plot()
    # plt.savefig("./layout.png",dpi=300,bbox_inches='tight')
    # plt.close("all")
    return sampling_areas

def main():

    # -- plot layouts --
    root = Path("./data/plot_layer/")
    plot_layout = load_plot_layout(root,'shp')

    # -- sampling area layer --
    root = Path("./data/sampling_areas/")
    sampling_areas = load_sampling_areas(root,'shp')

    # -- load example image
    img_path = "./data/NEPAC_L4_170801_200ft/DJI_1930.JPG"
    gps_coord = gpsphoto.getGPSData(img_path)
    raw_img = np.array(Image.open(img_path))

    fig,ax = plt.subplots(figsize=(8,8))
    print(sampling_areas.columns)
    print(plot_layout.columns)
    plot_layout.plot(ax=ax,alpha=0.5)
    sampling_areas.plot(column='Sarea_ID',ax=ax)

    plt.savefig("./sample_and_plot_layer.png",bbox_inches='tight')
    # print(sampling_areas.columns)
    # print(sampling_areas['geometry'].iloc[0])

if __name__ == "__main__":
    main()

