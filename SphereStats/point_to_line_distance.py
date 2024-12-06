import numpy as np
import matplotlib.pyplot as plt

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

# Shortest distance from point to line on a sphere
def point_to_line_distance(lat_p, lon_p, lat1, lon1, lat2, lon2, radius=EARTH_RADIUS):
    """Calculate the shortest distance from a point to a line on a sphere."""
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
    distance = radius * angle
    return distance

# Plot the sphere, points, and geodesic line
def plot_sphere_and_distance(lat_p, lon_p, lat1, lon1, lat2, lon2):
    """Plot a sphere, a geodesic line, and a point's shortest distance to the line."""
    # Create the sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot sphere
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.5, edgecolor='gray')

    # Convert points to Cartesian coordinates
    p = to_cartesian(lat_p, lon_p)
    l1 = to_cartesian(lat1, lon1)
    l2 = to_cartesian(lat2, lon2)

    # Plot the geodesic line
    t = np.linspace(0, 1, 100)
    geodesic = np.array([(1 - ti) * l1 + ti * l2 for ti in t])
    geodesic /= np.linalg.norm(geodesic, axis=1)[:, None] * EARTH_RADIUS
    ax.plot(geodesic[:, 0], geodesic[:, 1], geodesic[:, 2], color='green', label='Geodesic Line')

    # Plot the point
    ax.scatter(*p, color='red', s=100, label='Point (New Delhi)')

    # Calculate and plot the projection
    plane_normal = np.cross(l1, l2)
    plane_normal /= np.linalg.norm(plane_normal)
    projection = p - np.dot(p, plane_normal) * plane_normal
    projection /= np.linalg.norm(projection) * EARTH_RADIUS
    ax.scatter(*projection, color='purple', s=100, label='Projection onto Line')

    # Plot connecting line
    ax.plot([p[0], projection[0]], [p[1], projection[1]], [p[2], projection[2]], color='orange', label='Shortest Distance')

    # Add details to the plot
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_title("Point-to-Line Distance on a Sphere")
    ax.legend()
    plt.show()

# Example: New Delhi to London-Singapore geodesic line
lat_p, lon_p = 28.6139, 77.2090  # New Delhi
lat1, lon1 = 51.5074, -0.1278    # London
lat2, lon2 = 1.3521, 103.8198    # Singapore

# Calculate distance and plot
distance = point_to_line_distance(lat_p, lon_p, lat1, lon1, lat2, lon2)
plot_sphere_and_distance(lat_p, lon_p, lat1, lon1, lat2, lon2)

# Output the calculated distance
print(f"The shortest distance from the point to the line is: {distance:.2f} km")
