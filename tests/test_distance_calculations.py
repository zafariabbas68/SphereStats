import unittest
from math import sqrt
from SphereStats.distance_calculations import (
    geodetic_distance,
    euclidean_distance,
    spherical_to_cartesian,
    plot_distances,
)

class TestDistanceCalculations(unittest.TestCase):
    def test_geodetic_distance(self):
        # Test geodetic distance between known points
        nyc = (40.748817, -73.985428)  # Empire State Building
        la = (34.052235, -118.243683)  # Downtown Los Angeles
        expected_distance = 3940  # Approximate great-circle distance in km
        result = geodetic_distance(*nyc, *la)
        self.assertAlmostEqual(result, expected_distance, delta=50)

    def test_euclidean_distance(self):
        # Test Euclidean distance between known points
        nyc = (40.748817, -73.985428)
        la = (34.052235, -118.243683)
        result = euclidean_distance(*nyc, *la)
        self.assertGreater(result, 3800)
        self.assertLess(result, 4000)

    def test_spherical_to_cartesian(self):
        # Test Cartesian conversion
        nyc = (40.748817, -73.985428)
        x, y, z = spherical_to_cartesian(*nyc, radius=6371)
        self.assertAlmostEqual(sqrt(x**2 + y**2 + z**2), 6371, delta=1)

    def test_plot_generation(self):
        # Test if the plotting function runs without errors
        nyc = (40.748817, -73.985428)  # Empire State Building
        la = (34.052235, -118.243683)  # Downtown Los Angeles
        try:
            plot_distances(*nyc, *la)
        except Exception as e:
            self.fail(f"Plot generation failed with error: {e}")

if __name__ == "__main__":
    unittest.main()
