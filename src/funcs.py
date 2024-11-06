from osgeo import gdal
gdal.UseExceptions()
from typing import Union
from pathlib import Path
import shapely
import numpy as np
import geopandas as gpd

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