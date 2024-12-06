
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import unittest
import numpy as np
import matplotlib.pyplot as plt  # Import plt here to fix the NameError
from SphereStats.network_routing import (
    to_cartesian,
    haversine_distance,
    dijkstra,
    create_network,
    plot_network,
    plot_routes  # Added plot_routes import
)

class TestNetworkRouting(unittest.TestCase):

    def setUp(self):
        self.cities = [
            (40.7128, -74.0060),  # New York City
            (34.0522, -118.2437),  # Los Angeles
            (51.5074, -0.1278),    # London
            (48.8566, 2.3522),     # Paris
            (35.6895, 139.6917),   # Tokyo
        ]
        self.graph = create_network(self.cities)

    def test_haversine_distance(self):
        nyc = self.cities[0]
        la = self.cities[1]
        distance = haversine_distance(nyc, la)
        self.assertAlmostEqual(distance, 3940, delta=50)  # Approximate distance in km

    def test_dijkstra(self):
        start = self.cities[0]  # New York City
        goal = self.cities[3]   # Paris
        path, distance = dijkstra(self.graph, start, goal)
        self.assertIsNotNone(path)
        self.assertGreater(distance, 0)

    def test_create_network(self):
        self.assertIn(self.cities[0], self.graph)
        self.assertIn(self.cities[1], self.graph[self.cities[0]])

    def test_plot_network(self):
        """
        Test the plot_network function. This is primarily to ensure the function executes without errors.
        """
        try:
            start = self.cities[0]  # New York City
            goal = self.cities[3]   # Paris
            path, _ = dijkstra(self.graph, start, goal)
            plot_network(self.cities, path=path, graph=self.graph)
        except Exception as e:
            self.fail(f"plot_network raised an exception: {e}")

    def test_plot_routes(self):
        """
        Test the plot_routes function, plotting routes on different map projections.
        """
        lat1, lon1 = 40.748817, -73.985428  # New York
        lat2, lon2 = 34.052235, -118.243683  # Los Angeles
        try:
            plot_routes(lat1, lon1, lat2, lon2)
        except Exception as e:
            self.fail(f"plot_routes raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
