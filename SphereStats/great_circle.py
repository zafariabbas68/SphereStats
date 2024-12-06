# great_circle.py

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def great_circle_arc(lat1, lon1, lat2, lon2, num_points=100):
    """
    Calculate points along the great-circle arc between two geographical coordinates.
    Returns arrays of latitude and longitude points along the arc.
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Interpolate the great circle
    t = np.linspace(0, 1, num_points)
    d = 2 * np.arcsin(np.sqrt(np.sin((lat2 - lat1) / 2)**2 +
                              np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2)**2))
    A = np.sin((1 - t) * d) / np.sin(d)
    B = np.sin(t * d) / np.sin(d)

    x = A * np.cos(lat1) * np.cos(lon1) + B * np.cos(lat2) * np.cos(lon2)
    y = A * np.cos(lat1) * np.sin(lon1) + B * np.cos(lat2) * np.sin(lon2)
    z = A * np.sin(lat1) + B * np.sin(lat2)

    latitudes = np.arctan2(z, np.sqrt(x**2 + y**2))
    longitudes = np.arctan2(y, x)
    return np.degrees(latitudes), np.degrees(longitudes)

def plot_great_circle_arcs():
    """
    Generate a plot showing great-circle arcs between cities.
    """
    # Coordinates of example cities
    cities = {
        "New York": (40.7128, -74.0060),
        "Paris": (48.8566, 2.3522),
        "Tokyo": (35.6895, 139.6917),
        "Sydney": (-33.8688, 151.2093),
        "Los Angeles": (34.0522, -118.2437),
    }

    # Flat map with Mercator projection
    fig, ax = plt.subplots(figsize=(14, 10), subplot_kw={'projection': ccrs.PlateCarree()})

    # Set extent (lat/lon bounds) explicitly for global coverage
    ax.set_extent([-180, 180, -80, 80], crs=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray', linewidth=0.5)
    ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='black', linewidth=0.5)

    # Plot great-circle arcs between cities
    pairs = [("New York", "Paris"), ("Paris", "Tokyo"), ("Tokyo", "Sydney"), ("Sydney", "Los Angeles")]
    for city1, city2 in pairs:
        lat1, lon1 = cities[city1]
        lat2, lon2 = cities[city2]

        # Calculate the arc points
        arc_lat, arc_lon = great_circle_arc(lat1, lon1, lat2, lon2)
        ax.plot(arc_lon, arc_lat, transform=ccrs.Geodetic(), color='red', linewidth=2, label=f"{city1} to {city2}")

    # Plot city points
    for city, (lat, lon) in cities.items():
        ax.plot(lon, lat, marker='o', color='blue', markersize=8, transform=ccrs.PlateCarree())
        ax.text(lon + 3, lat - 2, city, transform=ccrs.PlateCarree(), fontsize=10, color='darkblue')

    # Add a title and legend
    ax.set_title('Great-Circle Arcs Between Cities (Flat Map)', fontsize=16)
    plt.legend(loc='upper left', fontsize=10, frameon=True)
    plt.show()
