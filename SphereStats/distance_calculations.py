# SphereStats/distance_calculations.py

import numpy as np
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

EARTH_RADIUS = 6371  # Default Earth radius in kilometers


def geodetic_distance(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """
    Calculate the geodetic distance (great-circle distance) using the haversine formula.
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return radius * c


def spherical_to_cartesian(lat, lon, radius=EARTH_RADIUS):
    """
    Convert spherical coordinates (latitude, longitude) to Cartesian coordinates.
    """
    x = radius * cos(lat) * cos(lon)
    y = radius * cos(lat) * sin(lon)
    z = radius * sin(lat)
    return x, y, z


def euclidean_distance(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """
    Calculate the Euclidean distance in 3D space between two points on a sphere.
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    x1, y1, z1 = spherical_to_cartesian(lat1, lon1, radius)
    x2, y2, z2 = spherical_to_cartesian(lat2, lon2, radius)
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def great_circle_path(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS, points=100):
    """
    Compute the great-circle path between two points on a sphere.
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    lats = np.linspace(lat1, lat2, points)
    lons = np.linspace(lon1, lon2, points)
    return np.array([spherical_to_cartesian(lat, lon, radius) for lat, lon in zip(lats, lons)])


def plot_distances(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """
    Visualize geodetic vs Euclidean distances between two points on a sphere.
    """
    x1, y1, z1 = spherical_to_cartesian(radians(lat1), radians(lon1), radius)
    x2, y2, z2 = spherical_to_cartesian(radians(lat2), radians(lon2), radius)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot sphere
    u, v = np.mgrid[0:2 * np.pi:100j, 0:np.pi:50j]
    xs = radius * np.cos(u) * np.sin(v)
    ys = radius * np.sin(u) * np.sin(v)
    zs = radius * np.cos(v)
    ax.plot_surface(xs, ys, zs, color='lightblue', alpha=0.3)

    # Plot points
    ax.scatter([x1, x2], [y1, y2], [z1, z2], color='red', s=100, label='Locations')
    ax.plot([x1, x2], [y1, y2], [z1, z2], label='Euclidean Distance', color='orange')

    # Geodetic path
    geodesic_path = great_circle_path(lat1, lon1, lat2, lon2, radius)
    ax.plot(geodesic_path[:, 0], geodesic_path[:, 1], geodesic_path[:, 2], label='Geodetic Path', color='green')

    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("Geodetic vs Euclidean Distance")
    ax.legend()
    plt.show()
