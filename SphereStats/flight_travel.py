# flight_travel.py

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Constants
EARTH_RADIUS = 6371  # in kilometers
FLIGHT_SPEED = 900  # Average commercial flight speed in km/h

# Function to calculate great-circle distance
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

# City coordinates
cities = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    "Sydney": (-33.8688, 151.2093),
    "Dubai": (25.276987, 55.296249),
}

# Function to calculate and plot flight paths between cities
def plot_flight_paths():
    # Calculate distances and travel times between cities
    travel_data = []
    pairs = [("New York", "London"), ("London", "Dubai"), ("Dubai", "Tokyo"), ("Tokyo", "Sydney")]

    for city1, city2 in pairs:
        lat1, lon1 = cities[city1]
        lat2, lon2 = cities[city2]
        distance = haversine_distance(lat1, lon1, lat2, lon2)
        travel_time = distance / FLIGHT_SPEED  # Time in hours
        travel_data.append((city1, city2, distance, travel_time))

    # Plot map with connections and travel times
    fig, ax = plt.subplots(figsize=(14, 10), subplot_kw={'projection': ccrs.PlateCarree()})

    # Set map extent
    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='black')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='black', linewidth=0.5)

    # Plot cities and connections
    for city, (lat, lon) in cities.items():
        ax.plot(lon, lat, marker='o', color='blue', markersize=8, transform=ccrs.PlateCarree())
        ax.text(lon + 3, lat - 3, city, transform=ccrs.PlateCarree(), fontsize=10, color='darkblue')

    # Draw great-circle arcs and annotate travel time
    for city1, city2, distance, travel_time in travel_data:
        lat1, lon1 = cities[city1]
        lat2, lon2 = cities[city2]

        # Draw great-circle arc as dashed line
        ax.plot(
            [lon1, lon2], [lat1, lat2],
            transform=ccrs.Geodetic(),
            color='red', linestyle='--', linewidth=2
        )

        # Annotate travel time at midpoint
        mid_lat = (lat1 + lat2) / 2
        mid_lon = (lon1 + lon2) / 2
        ax.text(
            mid_lon, mid_lat,
            f"{travel_time:.1f}h",
            transform=ccrs.Geodetic(),
            fontsize=10, color='darkred', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round')
        )

    # Add title
    ax.set_title('Flight Travel Times Between Cities', fontsize=16)

    # Display the plot in one single window
    plt.show()
