import unittest
from SphereStats.spherical_geometry import point_to_polygon_distance,  plot_sphere_and_polygon


class TestPointToPolygonDistance(unittest.TestCase):

    def test_point_to_polygon_distance(self):
        # Define a point and polygon
        lat_p, lon_p = 36.5, -121.0  # Point near the triangle
        polygon_coords = [
            (35.0, -120.0),  # First point of the polygon
            (37.0, -122.0),  # Second point of the polygon
            (36.0, -123.0)  # Third point of the polygon
        ]

        # Calculate the distance from the point to the polygon
        distance = point_to_polygon_distance(lat_p, lon_p, polygon_coords)

        # Assert the result is close to the expected distance (33.79 km)
        self.assertAlmostEqual(distance, 33.79, places=2)  # Updated expected value for point-to-polygon distance

        # Plot the sphere, point, and polygon
        plot_sphere_and_polygon(lat_p, lon_p, polygon_coords)  # Plot after the calculation


if __name__ == '__main__':
    unittest.main()
