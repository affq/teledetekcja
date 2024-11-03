from osgeo import gdal
gdal.UseExceptions()
from typing import Union
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely

def read_spatial_raster(path: Union[str, Path]) -> gdal.Dataset:
    dataset = gdal.Open(str(path))
    assert dataset is not None, "Read spatial raster returned None"
    return dataset

def points_to_pixels(points: np.ndarray, geotransform) -> np.ndarray:
    c, a, _, f, _, e = geotransform
    columns = (points[:, 0] - c) / a
    rows = (points[:, 1] - f) / e
    pixels = np.vstack([rows, columns])
    pixels = pixels.T
    return pixels

def reproject_geodataframe(features: gpd.GeoDataFrame, crs: str) -> gpd.GeoDataFrame:
    return features.to_crs(crs)

def convert_to_pixel_system(features: gpd.GeoDataFrame, geotransform) -> gpd.GeoDataFrame:
    def transform_function(xy: np.ndarray):
        ij = points_to_pixels(xy, geotransform)
        ji = ij[:, [1, 0]]
        return ji
    
    
    indices = features.index
    for i in indices:
        geometry = features.loc[i, "geometry"]
        geometry = shapely.transform(geometry, transform_function)
        features.loc[i, "geometry"] = geometry
    return features

def point_to_pixel(x, y, geotransform):
    c, a, b, f, d, e = geotransform
    column = (x - c) / a
    row = (y - f) / e
    return row, column  # ij convention to stay with NumPy

raster_file = r"TIFs\69815_306544_N-34-123-A-a-1-1.tif"
raster_dataset = read_spatial_raster(raster_file)    

band_1 = raster_dataset.GetRasterBand(1)
array_1 = band_1.ReadAsArray()
array_1 = np.copy(array_1)

band_2 = raster_dataset.GetRasterBand(2)
array_2 = band_2.ReadAsArray()
array_2 = np.copy(array_2)

band_3 = raster_dataset.GetRasterBand(3)
array_3 = band_3.ReadAsArray()
array_3 = np.copy(array_3)

vector_features = gpd.read_file(R"budynki1\budynki.shp")

features = reproject_geodataframe(vector_features, raster_dataset.GetProjection())
features = convert_to_pixel_system(features, raster_dataset.GetGeoTransform())

example_feature = features.iloc[0]
example_feature = example_feature['geometry']

bounds = example_feature.bounds
bounds = np.float64(bounds)

bounds[:2] = np.floor(bounds[:2])
bounds[2:] = np.ceil(bounds[2:])
bounds = np.int64(bounds)

fragment_1 = array_1[
    bounds[1]: bounds[3],
    bounds[0]: bounds[2]
]

fragment_2 = array_2[
    bounds[1]: bounds[3],
    bounds[0]: bounds[2]
]

fragment_3 = array_3[
    bounds[1]: bounds[3],
    bounds[0]: bounds[2]
]

rgb = np.dstack([fragment_1, fragment_2, fragment_3])
ndvi_fragment = (fragment_1 - fragment_2) / (fragment_1 + fragment_2)
ndvi_fragment[np.isnan(ndvi_fragment)] = 0
ndvi_fragment = ndvi_fragment/1 * 255
ndvi_fragment = np.uint8(ndvi_fragment)

ndvi = (array_1 - array_2)/ (array_1 + array_2)
ndvi[np.isnan(ndvi)] = 0
ndvi = ndvi/1 * 255
ndvi = np.uint8(ndvi)

plt.imshow(ndvi, cmap='gray')
plt.show()

plt.imshow(ndvi_fragment, cmap='gray')
plt.show()

import cv2
cv2.imwrite(R"ndvi.png", ndvi)
cv2.imwrite(R"ndvi_budynek.png", ndvi_fragment)