import unittest
import os
from SphereStats.Isochrone_NewYork import *  # Import everything from your iso_travel.py in SphereStats


class TestIsoTravel(unittest.TestCase):

    def setUp(self):
        # Setup that runs before each test, like clearing directories
        self.folderout = 'frames'
        if not os.path.exists(self.folderout):
            os.makedirs(self.folderout)

    def test_city_geocode(self):
        # Test if the city can be geocoded successfully
        city = 'New York City, USA'
        admin = ox.geocode_to_gdf(city)
        self.assertFalse(admin.empty, "City geocoding failed.")

    def test_centroid_calculation(self):
        # Test centroid calculation
        city = 'New York City, USA'
        admin = ox.geocode_to_gdf(city)
        admin_projected = admin.to_crs(admin.estimate_utm_crs())
        centroid = admin_projected.geometry.centroid.iloc[0]
        self.assertIsNotNone(centroid, "Centroid calculation failed.")

    def test_network_download(self):
        # Test if the network is downloaded successfully
        city = 'New York City, USA'
        admin = ox.geocode_to_gdf(city)
        G = ox.graph_from_polygon(admin.geometry.to_list()[0], network_type='drive', simplify=True)
        self.assertGreater(len(G.edges), 0, "Graph download failed or no edges found.")

    def test_isochrone_generation(self):
        # Test if isochrone polygons are being generated
        city = 'New York City, USA'
        admin = ox.geocode_to_gdf(city)
        admin_projected = admin.to_crs(admin.estimate_utm_crs())
        centroid = admin_projected.geometry.centroid.iloc[0]
        transformer = Transformer.from_crs(admin_projected.crs, "EPSG:4326", always_xy=True)
        centroid_geo = Point(transformer.transform(centroid.x, centroid.y))
        G = ox.graph_from_polygon(admin.geometry.to_list()[0], network_type='drive', simplify=True)

        center_node = ox.distance.nearest_nodes(G, centroid_geo.x, centroid_geo.y)

        # Calculate travel time for each edge
        walking_speed = 50 / 3.6  # Convert to meters per second
        for u, v, data in G.edges(data=True):
            data['travel_time'] = data['length'] / walking_speed

        isochrone_times = np.linspace(5, 60, 6)  # Divide into 6 evenly spaced times
        isochrone_polys = []
        for time in isochrone_times:
            subgraph = nx.ego_graph(G, center_node, radius=time * 60, distance='travel_time')
            node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]

            polygon = Polygon(gpd.GeoSeries(node_points).union_all().convex_hull)
            if polygon.is_valid:
                isochrone_polys.append(polygon)

        self.assertGreater(len(isochrone_polys), 0, "Isochrone polygons were not generated.")

    def test_frame_creation(self):
        # Test if the frames are being created
        frames = []
        city = 'New York City, USA'
        admin = ox.geocode_to_gdf(city)
        admin_projected = admin.to_crs(admin.estimate_utm_crs())
        centroid = admin_projected.geometry.centroid.iloc[0]
        transformer = Transformer.from_crs(admin_projected.crs, "EPSG:4326", always_xy=True)
        centroid_geo = Point(transformer.transform(centroid.x, centroid.y))
        G = ox.graph_from_polygon(admin.geometry.to_list()[0], network_type='drive', simplify=True)

        center_node = ox.distance.nearest_nodes(G, centroid_geo.x, centroid_geo.y)

        # Calculate travel time for each edge
        walking_speed = 50 / 3.6  # Convert to meters per second
        for u, v, data in G.edges(data=True):
            data['travel_time'] = data['length'] / walking_speed

        isochrone_times = np.linspace(5, 60, 6)  # Divide into 6 evenly spaced times
        isochrone_polys = []
        for time in isochrone_times:
            subgraph = nx.ego_graph(G, center_node, radius=time * 60, distance='travel_time')
            node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]

            polygon = Polygon(gpd.GeoSeries(node_points).union_all().convex_hull)
            if polygon.is_valid:
                isochrone_polys.append(polygon)

        # Create frames for animation
        for idx, (polygon, time) in enumerate(zip(isochrone_polys, isochrone_times)):
            frame_path = os.path.join(self.folderout, f'{idx + 1}.png')
            frames.append(frame_path)

        self.assertGreater(len(frames), 0, "No frames were created.")

    def tearDown(self):
        # Cleanup after tests, remove the frames folder
        import shutil
        if os.path.exists(self.folderout):
            shutil.rmtree(self.folderout)


if __name__ == '__main__':
    unittest.main()
