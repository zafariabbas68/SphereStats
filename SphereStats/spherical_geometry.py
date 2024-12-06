import numpy as np
import matplotlib.pyplot as plt
import numpy as np


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the Earth's surface."""
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    radius = 6371  # Earth's radius in kilometers
    distance = radius * c
    return distance


# Constants for Earth's radius
EARTH_RADIUS = 6371  # in kilometers


# Convert lat/lon to Cartesian coordinates
def to_cartesian(lat, lon, radius=EARTH_RADIUS):
    """Convert latitude and longitude to Cartesian coordinates."""
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return np.array([x, y, z])


# Calculate the shortest distance from a point to the nearest boundary of a polygon on a sphere
def point_to_polygon_distance(lat_p, lon_p, polygon_coords, radius=EARTH_RADIUS):
    """Calculate the shortest distance from a point to the nearest boundary of a polygon on a sphere."""
    # Convert the point to Cartesian coordinates
    p = to_cartesian(lat_p, lon_p, radius)

    # Initialize the minimum distance as a large value
    min_distance = float('inf')

    # Iterate over each edge of the polygon (pairs of consecutive points)
    for i in range(len(polygon_coords)):
        lat1, lon1 = polygon_coords[i]
        lat2, lon2 = polygon_coords[(i + 1) % len(polygon_coords)]  # Wrap around to the first point

        # Convert polygon points to Cartesian coordinates
        p1 = to_cartesian(lat1, lon1, radius)
        p2 = to_cartesian(lat2, lon2, radius)

        # Compute the shortest distance from the point to the edge (line segment)
        dist = point_to_line_distance(lat_p, lon_p, lat1, lon1, lat2, lon2, radius)

        # Update the minimum distance
        min_distance = min(min_distance, dist)

    return np.float64(min_distance)


# Compute the shortest distance from a point to a line (great-circle segment)
def point_to_line_distance(lat_p, lon_p, lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """Compute the shortest distance from a point to a line segment on the sphere."""
    # Convert points to Cartesian coordinates
    p = to_cartesian(lat_p, lon_p, radius)
    l1 = to_cartesian(lat1, lon1, radius)
    l2 = to_cartesian(lat2, lon2, radius)

    # Normalize to unit vectors
    p /= np.linalg.norm(p)
    l1 /= np.linalg.norm(l1)
    l2 /= np.linalg.norm(l2)

    # Compute the cross product of l1 and l2 (direction vector of great-circle plane)
    plane_normal = np.cross(l1, l2)
    plane_normal /= np.linalg.norm(plane_normal)

    # Project p onto the plane
    projection = p - np.dot(p, plane_normal) * plane_normal
    projection /= np.linalg.norm(projection)

    # Calculate angular distance between the projected point and the original point
    cos_angle = np.dot(p, projection)
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))  # Clip for numerical stability

    # Convert angular distance to linear distance
    distance = np.float64(radius * angle)  # Use np.float64 for the distance
    return distance


# Plot the sphere, point, polygon, and shortest distance
def plot_sphere_and_polygon(lat_p, lon_p, polygon_coords):
    """Plot a sphere with a point and a polygon on it, and the shortest distance from the point to the polygon."""
    # Create the sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot sphere with some transparency and a nice color
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.4, edgecolor='gray')

    # Convert the point and polygon vertices to Cartesian coordinates
    p = to_cartesian(lat_p, lon_p)
    polygon_cartesian = [to_cartesian(lat, lon) for lat, lon in polygon_coords]

    # Plot the point with larger size and distinct color
    ax.scatter(*p, color='orange', s=200, label='Point', marker='o', edgecolor='black', linewidth=2)

    # Plot the polygon edges
    for i in range(len(polygon_cartesian)):
        p1 = polygon_cartesian[i]
        p2 = polygon_cartesian[(i + 1) % len(polygon_cartesian)]  # Wrap around to the first point
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='green', lw=2)

    # Calculate and plot the shortest distance from the point to the polygon
    distance = point_to_polygon_distance(lat_p, lon_p, polygon_coords)
    print(f"The shortest distance from the point to the polygon is: {distance:.2f} km")

    # Add labels, title, and legend
    ax.set_box_aspect([1, 1, 1])  # Equal scaling for all axes
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("Point-to-Polygon Distance on a Sphere")
    ax.legend()

    # Show plot
    plt.show()
