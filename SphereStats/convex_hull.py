import numpy as np
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


# Helper function to convert spherical to Cartesian coordinates
def spherical_to_cartesian(lat, lon, radius=6371):
    lat, lon = np.radians(lat), np.radians(lon)
    x = radius * np.cos(lat) * np.cos(lon)
    y = radius * np.cos(lat) * np.sin(lon)
    z = radius * np.sin(lat)
    return np.array([x, y, z])


# Function to compute a convex hull on a sphere
def convex_hull_on_sphere(points):
    """
    Compute the convex hull of points on a sphere.

    Args:
    points: Array of latitude and longitude points [[lat1, lon1], [lat2, lon2], ...]

    Returns:
    hull_points: Indices of the points forming the convex hull
    """
    # Convert spherical to Cartesian coordinates
    cartesian_points = np.array([spherical_to_cartesian(lat, lon) for lat, lon in points])

    # Compute convex hull in Cartesian space
    hull = ConvexHull(cartesian_points)
    return hull, cartesian_points


# Function to visualize the convex hull in 3D
def plot_convex_hull_3d(hull, cartesian_points):
    """
    Visualize the convex hull in 3D.

    Args:
    hull: ConvexHull object
    cartesian_points: Cartesian coordinates of points
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the points
    ax.scatter(cartesian_points[:, 0], cartesian_points[:, 1], cartesian_points[:, 2], color='blue', label="Points")

    # Plot the convex hull
    for simplex in hull.simplices:
        simplex = np.append(simplex, simplex[0])  # Close the polygon
        ax.plot(cartesian_points[simplex, 0], cartesian_points[simplex, 1], cartesian_points[simplex, 2], color="red")

    # Plot hull faces
    ax.add_collection3d(Poly3DCollection(cartesian_points[hull.simplices], facecolors='red', alpha=0.2))

    # Make it spherical
    max_radius = np.max(np.linalg.norm(cartesian_points, axis=1))
    ax.set_xlim([-max_radius, max_radius])
    ax.set_ylim([-max_radius, max_radius])
    ax.set_zlim([-max_radius, max_radius])
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    plt.title("Convex Hull on a Sphere (3D)")
    plt.legend()
    plt.show()


# Function to plot convex hull in 2D projection
def plot_convex_hull_2d(points, hull, projection=ccrs.Mollweide()):
    """
    Visualize the convex hull on a 2D map projection.

    Args:
    points: Original spherical points [[lat1, lon1], [lat2, lon2], ...]
    hull: ConvexHull object
    projection: Cartopy projection for visualization
    """
    fig = plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=projection)
    ax.set_global()
    ax.stock_img()
    ax.coastlines()

    # Plot all points
    lats, lons = zip(*points)
    ax.scatter(lons, lats, transform=ccrs.PlateCarree(), color='blue', label="Points")

    # Plot convex hull edges
    for simplex in hull.simplices:
        hull_points = np.array([points[simplex[0]], points[simplex[1]]])
        ax.plot(hull_points[:, 1], hull_points[:, 0], transform=ccrs.PlateCarree(), color='red')

    plt.title("Convex Hull on a 2D Projection")
    plt.legend()
    plt.show()


# Example usage
if __name__ == "__main__":
    # Define random points on a sphere (latitude, longitude in degrees)
    points = np.array([
        [40.748817, -73.985428],  # New York
        [34.052235, -118.243683],  # Los Angeles
        [48.8566, 2.3522],  # Paris
        [-33.8688, 151.2093],  # Sydney
        [35.6895, 139.6917],  # Tokyo
        [51.5074, -0.1278],  # London
        [-23.5505, -46.6333],  # São Paulo
        [55.7558, 37.6173],  # Moscow
    ])

    # Compute convex hull
    hull, cartesian_points = convex_hull_on_sphere(points)

    # Visualize the convex hull
    plot_convex_hull_3d(hull, cartesian_points)
    plot_convex_hull_2d(points, hull)
