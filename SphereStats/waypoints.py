import numpy as np
import matplotlib.pyplot as plt

EARTH_RADIUS = 6371  # Earth's radius in kilometers

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
    return R * c

def interpolate_waypoints(start, end, num_points=5):
    start_cartesian = to_cartesian(*start)
    end_cartesian = to_cartesian(*end)
    start_cartesian /= np.linalg.norm(start_cartesian)
    end_cartesian /= np.linalg.norm(end_cartesian)

    waypoints = []
    for i in range(num_points):
        t = i / (num_points - 1)
        point = (1 - t) * start_cartesian + t * end_cartesian
        point /= np.linalg.norm(point)
        lat = np.degrees(np.arcsin(point[2]))
        lon = np.degrees(np.arctan2(point[1], point[0]))
        waypoints.append((lat, lon))
    return waypoints

def total_travel_distance(waypoints):
    total_distance = 0
    for i in range(1, len(waypoints)):
        total_distance += haversine_distance(waypoints[i-1], waypoints[i])
    return total_distance

def plot_waypoints(start, end, waypoints):
    latitudes, longitudes = zip(start, end)
    latitudes = np.append(latitudes, [wp[0] for wp in waypoints])
    longitudes = np.append(longitudes, [wp[1] for wp in waypoints])

    plt.figure(figsize=(10, 8))
    plt.scatter(longitudes, latitudes, color='blue', label="Waypoints")
    for wp in waypoints:
        plt.text(wp[1] + 0.1, wp[0], f"({wp[0]:.2f}, {wp[1]:.2f})", fontsize=12)
    plt.plot(longitudes, latitudes, color='red', label="Route")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Waypoints Along the Route')
    plt.legend()
    plt.grid(True)
    plt.show()
