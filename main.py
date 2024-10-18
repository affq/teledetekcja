import numpy

from osgeo import gdal
gdal.UseExceptions()

from typing import Union
from pathlib import Path
def read_spatial_raster(path: Union[str, Path]) -> gdal.Dataset:
    dataset = gdal.Open(str(path))
    assert dataset is not None, "Read spatial raster returned None"
    return dataset

raster_file = "N-34-A-a-1-1.tif"
raster_dataset = read_spatial_raster(raster_file)    
print("Natywny układ współrzędnych rastra:", 
raster_dataset.GetProjection())
print("Patametry transformacji z układu XY do układu UV rastra:", 
raster_dataset.GetGeoTransform())
print("ok")
exit()

print("Liczba kanałów:", raster_dataset.RasterCount)
print("Wymiary rastra w pikselach (szerokość x wysokość):", 
[raster_dataset.RasterXSize, raster_dataset.RasterYSize])