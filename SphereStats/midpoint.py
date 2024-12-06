import numpy as np
import matplotlib.pyplot as plt

# Earth's radius in kilometers
EARTH_RADIUS = 6371

def to_cartesian(lat, lon, radius=EARTH_RADIUS):
    """
    Convert latitude and longitude to Cartesian coordinates.
    """
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return np.array([x, y, z])

def midpoint(lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """
    Calculate the Cartesian midpoint between two geographic points on a sphere.
    """
    p1 = to_cartesian(lat1, lon1, radius)
    p2 = to_cartesian(lat2, lon2, radius)
    midpoint_cartesian = (p1 + p2) / np.linalg.norm(p1 + p2)  # Normalize to unit vector
    return midpoint_cartesian * radius  # Scale to sphere's radius

def plot_sphere_with_midpoint(lat1, lon1, lat2, lon2):
    """
    Plot a sphere with two points and their midpoint.
    """
    # Create the sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the sphere
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.5, edgecolor='gray')

    # Compute Cartesian coordinates for the points
    p1 = to_cartesian(lat1, lon1)
    p2 = to_cartesian(lat2, lon2)
    midpoint_cartesian = midpoint(lat1, lon1, lat2, lon2)

    # Plot points and midpoint
    ax.scatter(*p1, color='red', s=100, label="Point 1", marker='o')
    ax.scatter(*p2, color='blue', s=100, label="Point 2", marker='o')
    ax.scatter(*midpoint_cartesian, color='green', s=150, label="Midpoint", marker='X')

    # Add labels, legend, and title
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("Midpoint Between Two Points on a Sphere")
    ax.legend()

    plt.show()

# Example usage: New York City and Los Angeles
if __name__ == "__main__":
    lat1, lon1 = 40.7128, -74.0060  # New York City
    lat2, lon2 = 34.0522, -118.2437  # Los Angeles
    plot_sphere_with_midpoint(lat1, lon1, lat2, lon2)
