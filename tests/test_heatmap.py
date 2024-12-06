# tests/test_heatmap.py

import unittest
import sys
import os
import numpy as np  # Add numpy import here

# Add your library path to the Python path for testing
sys.path.insert(0, os.path.abspath('/Users/ghulamabbaszafari/Desktop/SphereStats'))

from SphereStats.heatmap import haversine, generate_heatmap

# Define EARTH_RADIUS here
EARTH_RADIUS = 6371  # Earth's radius in kilometers

# Shapefile paths for testing
shapefile_countries = "/Users/ghulamabbaszafari/Downloads/packages/Natural_Earth_quick_start/110m_cultural/ne_110m_admin_0_countries.shp"
shapefile_boundaries = "/Users/ghulamabbaszafari/Downloads/packages/Natural_Earth_quick_start/110m_cultural/ne_110m_admin_0_boundary_lines_land.shp"
origin = (40.7128, -74.0060)  # New York City coordinates

class TestHeatmap(unittest.TestCase):

    def test_haversine(self):
        # Test distance between New York and Los Angeles
        nyc = (40.7128, -74.0060)
        la = (34.0522, -118.2437)
        distance = haversine(nyc[0], nyc[1], la[0], la[1])
        self.assertAlmostEqual(distance, 3940, delta=10)  # Expected ~3940 km

    def test_haversine_same_point(self):
        # Distance from a point to itself should be zero
        point = (40.7128, -74.0060)
        self.assertEqual(haversine(point[0], point[1], point[0], point[1]), 0)

    def test_haversine_opposite_poles(self):
        # Test distance between the North and South Poles
        north_pole = (90, 0)
        south_pole = (-90, 0)
        distance = haversine(north_pole[0], north_pole[1], south_pole[0], south_pole[1])
        self.assertAlmostEqual(distance, EARTH_RADIUS * np.pi, delta=10)  # Half circumference

    def test_generate_heatmap(self):
        # Test the generate_heatmap function with the shapefiles and origin
        # This test won't return anything, but will check for any errors in running the function
        try:
            generate_heatmap(shapefile_countries, shapefile_boundaries, origin)
        except Exception as e:
            self.fail(f"generate_heatmap raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
