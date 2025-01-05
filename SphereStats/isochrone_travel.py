# From your own library (SphereStats)
from SphereStats.flight_travel import haversine_distance
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import Point
from shapely.ops import unary_union
import geopandas as gpd
from matplotlib.patches import Patch

# Constants for the isochrone functionality
EARTH_RADIUS = 6371  # in kilometers
TRAVEL_SPEED = 60  # Speed in km/h (assumed constant)
TIME_THRESHOLDS = [1, 2, 3]  # Travel time thresholds in hours

# Function to calculate haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth (in km).
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return EARTH_RADIUS * c

def generate_isochrones(center_lat, center_lon, time_thresholds):
    """
    Generate isochrones based on time thresholds.
    Returns a list of GeoDataFrames representing isochrones.
    """
    # Generate grid points around the center location
    lats = np.linspace(center_lat - 5, center_lat + 5, 200)
    lons = np.linspace(center_lon - 5, center_lon + 5, 200)
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Calculate distances and travel times for each point in the grid
    distances = haversine_distance(center_lat, center_lon, lat_grid, lon_grid)
    travel_times = distances / TRAVEL_SPEED  # Time in hours

    # Create polygons for isochrones
    isochrones = []
    for threshold in time_thresholds:
        mask = travel_times <= threshold
        points_within = [
            Point(lon, lat) for lon, lat, within in zip(lon_grid.flatten(), lat_grid.flatten(), mask.flatten()) if within
        ]
        isochrones.append(unary_union([point.buffer(0.1) for point in points_within]))  # Approximate regions

    # Convert to GeoDataFrames
    iso_gdfs = [gpd.GeoDataFrame(geometry=[iso], crs="EPSG:4326") for iso in isochrones]
    return iso_gdfs

def plot_isochrones():
    """
    Plot the isochrones generated from the center location.
    """
    # Set up the central location (New York City)
    center_lat, center_lon = 40.7128, -74.0060

    # Generate isochrones
    isochrones = generate_isochrones(center_lat, center_lon, TIME_THRESHOLDS)

    # Plot the isochrones on a map
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([-80, -70, 35, 45], crs=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.COASTLINE, edgecolor='black')
    ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='black')

    # Plot isochrones
    colors = ['green', 'orange', 'red']
    labels = [f"{threshold} hr" for threshold in TIME_THRESHOLDS]
    for iso_gdf, color in zip(isochrones, colors):
        iso_gdf.plot(ax=ax, color=color, alpha=0.4)

    # Mark the central point
    ax.plot(center_lon, center_lat, marker='o', color='blue', markersize=8, transform=ccrs.PlateCarree(), label="New York")

    # Add a custom legend
    legend_patches = [Patch(color=color, label=label) for color, label in zip(colors, labels)]
    ax.legend(handles=legend_patches + [Patch(facecolor='blue', edgecolor='blue', label='New York')],
              loc="lower left", fontsize=10)

    # Add title
    ax.set_title('Isochrones: Areas Reachable from New York', fontsize=16)

    plt.show()



