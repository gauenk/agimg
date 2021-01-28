# -- python imports --
import glob,cv2
from easydict import EasyDict as edict
from PIL import Image
from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from GPSPhoto import gpsphoto
from shapely.geometry import Point,Polygon
from descartes import PolygonPatch

import rasterio
import rasterio.plot


# -- project imports --
import _init_paths
from pyutils.vgi import compute_vgi
from pyutils.misc import get_xyz
from pyutils.utm import project
from datasets.fall_2020_data import load_plot_layout,load_sampling_areas,load_large_tif_filename,find_reference_point,normalize_to_reference

def main():

    # -- load shape data --
    root = Path("./data")
    plot_layout = load_plot_layout(root)
    sampling_areas = load_sampling_areas(root)

    # -- load image data --
    img_fn = load_large_tif_filename(root)
    # Image.MAX_IMAGE_PIXELS = 1 << 36
    # img = Image.open(img_fn)
    # img = np.array(img)
    img = rasterio.open(img_fn)
    print(img.bounds)
    print(img.crs)
    print(img.transform)
    print(img._transform)
    lat,lon = img._transform[3],img._transform[0]
    z,l,lon,lat = project([lon,lat])
    img._transform[3],img._transform[0] = lat,lon
    # img._transform[3],img._transform[0] = 0,0
    # img._transform[1],img._transform[5] = 1.,-1.
    # pixel_scale = np.sqrt(img._transform[1])
    # img._transform[1],img._transform[5] = pixel_scale,-pixel_scale
    # print(img.transform)
    # pixel_scale = (3.04768227457637e-07, 3.04768227457637e-07)

    # -- gps projection --
    plot_layout = plot_layout.to_crs('EPSG:32616')
    sampling_areas = sampling_areas.to_crs('EPSG:32616')
    ref_point = find_reference_point(plot_layout)
    print(ref_point,(lon,lat))

    # -- normalize geometry --
    # plot_layout['geometry'] = normalize_to_reference(plot_layout['geometry'],ref_point,pixel_scale)
    # sampling_areas['geometry'] = normalize_to_reference(sampling_areas['geometry'],ref_point,pixel_scale)
                
    # print(plot_layout['geometry'].iloc[0])
    print(sampling_areas['geometry'].iloc[0])

    # -- memory mapping --
    # npy_fn = Path(str(img_fn).split(".")[0] + ".npy")
    # img = Image.open(img_fn)
    # img = np.array(img).reshape(22530,14961)
    # np.save(npy_fn,img,allow_pickle=False)
    # fp = np.memmap(npy_fn)
    # fp = np.memmap(npy_fn,dtype="float32",mode="w",shape=(22530,14961))
    # fp[...] = img[...]
    # fp.flush()
    # fp.close()
    
    
    # -- downsample image --
    # new_shape = (22530 // 10 , 14961 // 10)
    # plt_img = cv2.resize(data, new_shape, interpolation=cv2.INTER_CUBIC)

    # -- plot sampling area and plot layout --
    # fig,ax = plt.subplots(figsize=(8,8))
    # plot_layout.plot(ax=ax,alpha=0.5)
    # sampling_areas.plot(column='Sarea_ID',ax=ax)
    # ax.imshow(img)
    # plt.show()
    # plt.savefig("./output/sample_and_plot_layer_proj.png",transparent=True,bbox_inches='tight')
    # plt.close("all")

    # -- rasterio plotting --
    fig,ax = plt.subplots(figsize=(8,8))
    plot_layout.plot(ax=ax,alpha=0.5)
    sampling_areas.plot(ax=ax,column='Sarea_ID')
    print(ax.get_ylim(),ax.get_xlim())
    ymin_a,ymax_a = min(ax.get_ylim()),max(ax.get_ylim())
    xmin_a,xmax_a = min(ax.get_xlim()),max(ax.get_xlim())
    rasterio.plot.show(img,ax=ax)
    print(ax.get_ylim(),ax.get_xlim())
    ymin_b,ymax_b = min(ax.get_ylim()),max(ax.get_ylim())
    xmin_b,xmax_b = min(ax.get_xlim()),max(ax.get_xlim())
    ymin,ymax = min([ymin_a,ymin_b]),max([ymax_a,ymax_b])
    xmin,xmax = min([xmin_a,xmin_b]),max([xmax_a,xmax_b])
    print((ymin,ymax),(xmin,xmax))
    ax.set_ylim(ymin,ymax)
    ax.set_xlim(xmin,xmax)
    # ax.imshow(img)
    # patches = [PolygonPatch(poly,edgecolor="red", facecolor="none", linewidth=2) for poly in sampling_areas['geometry']]
    # patches = [PolygonPatch(sampling_areas['geometry'])]
    # ax.add_collection(mpl.collections.PatchCollection(patches, match_original=True))
    plt.savefig("./output/vis_large_image.png")


if __name__ == "__main__":
    main()
