import numpy as np
import matplotlib.pyplot as plt

def to_cartesian(lat, lon, radius=1):
    """Convert latitude and longitude to Cartesian coordinates."""
    lat, lon = np.radians(lat), np.radians(lon)
    return np.array([
        radius * np.cos(lat) * np.cos(lon),  # x
        radius * np.cos(lat) * np.sin(lon),  # y
        radius * np.sin(lat)                 # z
    ])

def haversine(lat1, lon1, lat2, lon2, radius=6371):
    """Calculate the great-circle distance using the Haversine formula."""
    lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    return radius * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

def plot_great_circle_with_stats(lat1, lon1, lat2, lon2):
    """Plot a great-circle path between two points on a sphere and display the distance."""
    # Generate sphere coordinates
    phi, theta = np.mgrid[0:2 * np.pi:100j, 0:np.pi:50j]
    x, y, z = np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)

    # Convert points to Cartesian coordinates
    p1, p2 = to_cartesian(lat1, lon1), to_cartesian(lat2, lon2)

    # Interpolate and normalize the great-circle path
    path = np.array([(1 - t) * p1 + t * p2 for t in np.linspace(0, 1, 100)])
    path /= np.linalg.norm(path, axis=1)[:, None]  # Normalize to unit sphere

    # Calculate great-circle distance
    distance_km = haversine(lat1, lon1, lat2, lon2)

    # Plot the 3D sphere and the great-circle path
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, color='lightblue', alpha=0.5, edgecolor='gray')  # Sphere
    ax.plot(path[:, 0], path[:, 1], path[:, 2], color='red', linewidth=2, label='Great-Circle Path')  # Path

    # Plot the two points
    ax.scatter(*p1, color='green', s=100, label=f'Point 1: ({lat1}, {lon1})')
    ax.scatter(*p2, color='blue', s=100, label=f'Point 2: ({lat2}, {lon2})')

    # Formatting the plot
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.grid(True)
    ax.legend(loc='upper right')

    # Display distance outside the plot
    fig.text(0.1, 0.02, f"Great-Circle Distance: {distance_km:.6f} km", fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

    plt.show()
