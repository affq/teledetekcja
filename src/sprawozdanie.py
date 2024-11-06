import matplotlib.pyplot as plt
from funcs import *

cir_raster = r"TIFs\CIR_2015.tif"
cir_dataset = read_spatial_raster(cir_raster)

band_nir = cir_dataset.GetRasterBand(1)
array_nir = band_nir.ReadAsArray()
array_nir = np.copy(array_nir)

band_red = cir_dataset.GetRasterBand(2)
array_red = band_red.ReadAsArray()
array_red = np.copy(array_red)

band_green = cir_dataset.GetRasterBand(3)
array_green = band_green.ReadAsArray()
array_green = np.copy(array_green)

rgb_raster = r"TIFs\RGB_2015.tif"
rgb_dataset = read_spatial_raster(rgb_raster)

band_blue = rgb_dataset.GetRasterBand(3)
array_blue = band_blue.ReadAsArray()
array_blue = np.copy(array_blue)

vector_features = gpd.read_file(R"budynki\budynki.shp")

features = reproject_geodataframe(vector_features, cir_dataset.GetProjection())
features = convert_to_pixel_system(features, cir_dataset.GetGeoTransform())

ids = np.array([7, 0, 3])

for id in ids:
    example_feature = features.iloc[id]
    example_feature = example_feature['geometry']

    bounds = example_feature.bounds
    bounds = np.float64(bounds)

    bounds[:2] = np.floor(bounds[:2])
    bounds[2:] = np.ceil(bounds[2:])
    bounds = np.int64(bounds)

    fragment_nir = array_nir[
        bounds[1]: bounds[3],
        bounds[0]: bounds[2]
    ]

    fragment_red = array_red[
        bounds[1]: bounds[3],
        bounds[0]: bounds[2]
    ]

    fragment_green = array_green[
        bounds[1]: bounds[3],
        bounds[0]: bounds[2]
    ]

    fragment_blue = array_blue[
        bounds[1]: bounds[3],
        bounds[0]: bounds[2]
    ]

    plt.imsave(f"img\\nir_budynek{id}.png", fragment_nir, cmap='gray')
    plt.imsave(f"img\\red_budynek{id}.png", fragment_red, cmap='gray')
    plt.imsave(f"img\green_budynek{id}.png", fragment_green, cmap='gray')
    plt.imsave(f"img\\blue_budynek{id}.png", fragment_blue, cmap='gray')


