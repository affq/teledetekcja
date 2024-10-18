from email.message import EmailMessage
from osgeo import gdal
gdal.UseExceptions()
from typing import Union
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

def read_spatial_raster(path: Union[str, Path]) -> gdal.Dataset:
    dataset = gdal.Open(str(path))
    assert dataset is not None, "Read spatial raster returned None"
    return dataset

raster_file = "N-34-111-A-a-1-1.tif"
raster_dataset = read_spatial_raster(raster_file)    

band = raster_dataset.GetRasterBand(1)
array = band.ReadAsArray()
array = np.copy(array)

vector_features = gpd.read_file(R"budynki1\budynki.shp")
example_point = vector_features.iloc[0]['geometry'].centroid.xy
example_point = np.float64(example_point)

def point_to_pixel(x, y, geotransform):
    c, a, b, f, d, e = geotransform
    column = (x - c) / a
    row = (y - f) / e
    return row, column  # ij convention to stay with NumPy

i, j = point_to_pixel(example_point[0], example_point[1], raster_dataset.GetGeoTransform())

plt.imshow(array, cmap='grey')
plt.scatter(j, i)
plt.show()