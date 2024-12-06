import numpy as np

# Constants for Earth's radius
EARTH_RADIUS = 6371  # in kilometers

def to_cartesian(lat, lon, radius=EARTH_RADIUS):
    """Convert latitude and longitude to Cartesian coordinates."""
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return np.array([x, y, z])

def midpoint(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """Calculate the midpoint between two points on the sphere."""
    p1 = to_cartesian(lat1, lon1, radius)
    p2 = to_cartesian(lat2, lon2, radius)
    midpoint_cartesian = (p1 + p2) / np.linalg.norm(p1 + p2)  # Normalize to unit vector
    return midpoint_cartesian * radius  # Scale to sphere's radius

def example_usage():
    lat1, lon1 = 40.7128, -74.0060  # New York City
    lat2, lon2 = 34.0522, -118.2437  # Los Angeles
    plot_sphere_with_midpoint(lat1, lon1, lat2, lon2)

