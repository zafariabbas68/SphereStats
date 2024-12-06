# SphereStats/heatmap.py

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from matplotlib.colors import Normalize

EARTH_RADIUS = 6371  # Earth's radius in kilometers

# Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return EARTH_RADIUS * c

# Heatmap generation
def generate_heatmap(shapefile_countries, shapefile_boundaries, origin):
    lon = np.linspace(-180, 180, 360)
    lat = np.linspace(-90, 90, 180)
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    distances = haversine(origin[0], origin[1], lat_grid, lon_grid)
    norm = Normalize(vmin=0, vmax=np.percentile(distances, 95))

    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

    heatmap = ax.pcolormesh(lon, lat, distances, transform=ccrs.PlateCarree(),
                            cmap='YlOrRd', norm=norm, alpha=0.6)

    reader_countries = shpreader.Reader(shapefile_countries)
    countries_feature = cfeature.ShapelyFeature(reader_countries.geometries(), ccrs.PlateCarree())

    reader_boundaries = shpreader.Reader(shapefile_boundaries)
    boundaries_feature = cfeature.ShapelyFeature(reader_boundaries.geometries(), ccrs.PlateCarree())

    ax.add_feature(countries_feature, facecolor='none', edgecolor='black', linewidth=0.7, alpha=0.8)
    ax.add_feature(boundaries_feature, facecolor='none', edgecolor='blue', linewidth=0.5, alpha=0.6)

    cbar = plt.colorbar(heatmap, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
    cbar.set_label('Distance (km) from Origin')

    ax.set_title('Heatmap of Distances from Origin', fontsize=16)
    plt.show()
