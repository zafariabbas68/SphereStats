import numpy as np
import heapq
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.geodesic import Geodesic

EARTH_RADIUS = 6371  # in kilometers

def to_cartesian(lat, lon, radius=EARTH_RADIUS):
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return np.array([x, y, z])

def haversine_distance(p1, p2):
    R = EARTH_RADIUS
    dlat = np.radians(p2[0] - p1[0])
    dlon = np.radians(p2[1] - p1[1])

    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(p1[0])) * np.cos(np.radians(p2[0])) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance

def dijkstra(graph, start, goal):
    queue = [(0, start)]
    distances = {start: 0}
    previous_nodes = {start: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == goal:
            path = []
            while previous_nodes[current_node] is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            path.append(start)
            path.reverse()
            return path, distances[goal]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return None, float("inf")

def create_network(cities):
    graph = {city: {} for city in cities}
    for i, city1 in enumerate(cities):
        for j, city2 in enumerate(cities):
            if i != j:
                distance = haversine_distance(city1, city2)
                graph[city1][city2] = distance
    return graph

def plot_network(cities, path=None, graph=None):
    latitudes, longitudes = zip(*cities)
    city_names = ['New York', 'Los Angeles', 'London', 'Paris', 'Tokyo']

    plt.figure(figsize=(10, 8))
    plt.scatter(longitudes, latitudes, color='blue', label='Cities')
    for i, city in enumerate(cities):
        plt.text(longitudes[i] + 0.1, latitudes[i], city_names[i], fontsize=12)
    if graph:
        for city1, neighbors in graph.items():
            for city2 in neighbors:
                plt.plot([city1[1], city2[1]], [city1[0], city2[0]], color='gray', linewidth=0.5)
    if path:
        path_lats, path_lons = zip(*path)
        plt.plot(path_lons, path_lats, color='red', marker='o', label="Shortest Path")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Shortest Path Between Cities')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to plot routes on different projections
def plot_routes(lat1, lon1, lat2, lon2):
    """
    Plot the great-circle route between two points on different map projections.

    Args:
    lat1, lon1: Latitude and Longitude of the first point (degrees)
    lat2, lon2: Latitude and Longitude of the second point (degrees)
    """
    # Create a figure
    fig = plt.figure(figsize=(16, 10))

    # Define map projections to visualize
    projections = {
        "Mercator Projection": ccrs.Mercator(),
        "Mollweide Projection": ccrs.Mollweide(),
        "PlateCarree Projection": ccrs.PlateCarree()
    }

    # Iterate over projections
    for i, (name, proj) in enumerate(projections.items(), 1):
        ax = fig.add_subplot(2, 2, i, projection=proj)
        ax.set_title(name)
        ax.stock_img()  # Add a simple background image of Earth
        ax.coastlines()

        # Use Cartopy's Geodesic class to calculate great-circle paths
        geodesic = Geodesic()
        great_circle = geodesic.inverse([lon1, lon2], [lat1, lat2])

        # Extract the great-circle path
        lons, lats = great_circle[:, 0], great_circle[:, 1]

        # Plot the path
        ax.plot(lons, lats, color='red', transform=ccrs.Geodetic(), label="Great-Circle Route")
        ax.scatter([lon1, lon2], [lat1, lat2], color='blue', transform=ccrs.PlateCarree(), zorder=5, label="Locations")

        # Add a legend
        ax.legend(loc="lower left")

    # Show the plot
    plt.tight_layout()
    plt.show()
