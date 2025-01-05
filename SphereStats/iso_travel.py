import os
import osmnx as ox
import numpy as np
import networkx as nx
from shapely.geometry import Point, Polygon
import geopandas as gpd
import matplotlib.pyplot as plt
from PIL import Image
from pyproj import Transformer


# Skip plotting and gif creation in test mode
def generate_isochrones(skip_plots=True):
    # Output folder for frames
    folderout = 'frames'
    if not os.path.exists(folderout):
        os.makedirs(folderout)

    # City configuration
    city = 'New York City, USA'
    admin = ox.geocode_to_gdf(city)
    admin_projected = admin.to_crs(admin.estimate_utm_crs())
    centroid = admin_projected.geometry.centroid.iloc[0]

    # Transform centroid back to geographic coordinates
    transformer = Transformer.from_crs(admin_projected.crs, "EPSG:4326", always_xy=True)
    centroid_geo = Point(transformer.transform(centroid.x, centroid.y))

    # Download the road network
    G = ox.graph_from_polygon(admin.geometry.to_list()[0], network_type='drive', simplify=True)

    # Find the nearest node to the centroid
    center_node = ox.distance.nearest_nodes(G, centroid_geo.x, centroid_geo.y)

    # Calculate travel time for each edge
    walking_speed = 50 / 3.6  # Convert to meters per second
    for u, v, data in G.edges(data=True):
        data['travel_time'] = data['length'] / walking_speed

    # Isochrone times (in minutes)
    isochrone_times = np.linspace(5, 60, 6)  # Divide into 6 evenly spaced times
    isochrone_polys = []

    for time in isochrone_times:
        subgraph = nx.ego_graph(G, center_node, radius=time * 60, distance='travel_time')
        node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]
        polygon = Polygon(gpd.GeoSeries(node_points).union_all().convex_hull)

        # Ensure the polygon is valid
        if polygon.is_valid:
            isochrone_polys.append(polygon)

    if not isochrone_polys:
        print("Error: No valid isochrone polygons generated.")
    else:
        print(f"Generated {len(isochrone_polys)} valid isochrone polygons.")

    # Skip plotting and gif creation in test mode
    if skip_plots:
        return isochrone_polys

    # If plotting and GIF generation are needed, you can add the plotting logic here as before.
    frames = []
    for idx, (polygon, time) in enumerate(zip(isochrone_polys, isochrone_times)):
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        # Plot the data here as needed (e.g., roads, polygons)
        frames.append(Image.open("frame.png"))  # Sample code for frame appending (update if needed)

    # Create animated GIF (if necessary)
    gif_path = 'newyork_isochrones.gif'
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=1000,
        loop=0
    )
    print(f'Animation saved at {gif_path}')


# Example test for generating isochrones
def test_generate_isochrones():
    # Call generate_isochrones with skip_plots=True
    result = generate_isochrones(skip_plots=True)
    assert len(result) > 0, "No isochrones generated."
    print("Isochrones generated successfully.")


# Run the test
if __name__ == "__main__":
    test_generate_isochrones()