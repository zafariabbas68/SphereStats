import unittest
from SphereStats.midpoint import to_cartesian, midpoint, plot_sphere_with_midpoint


class TestMidpoint(unittest.TestCase):

    def test_to_cartesian(self):
        # Test known values
        lat, lon = 0, 0  # Equator, Prime Meridian
        result = to_cartesian(lat, lon)
        expected = [6371, 0, 0]  # Earth's radius in x-axis
        self.assertAlmostEqual(result[0], expected[0], places=2)
        self.assertAlmostEqual(result[1], expected[1], places=2)
        self.assertAlmostEqual(result[2], expected[2], places=2)

    def test_midpoint(self):
        # Test midpoint between New York and Los Angeles
        lat1, lon1 = 40.7128, -74.0060  # New York City
        lat2, lon2 = 34.0522, -118.2437  # Los Angeles
        midpoint_result = midpoint(lat1, lon1, lat2, lon2)

        # Check that the midpoint is a valid point on the sphere
        radius = (midpoint_result[0] ** 2 + midpoint_result[1] ** 2 + midpoint_result[2] ** 2) ** 0.5
        self.assertAlmostEqual(radius, 6371, places=2)  # Should be close to Earth's radius

    def test_plot_sphere_with_midpoint(self):
        # Plot sphere with New York City and Los Angeles
        lat1, lon1 = 40.7128, -74.0060
        lat2, lon2 = 34.0522, -118.2437
        plot_sphere_with_midpoint(lat1, lon1, lat2, lon2)  # This should show the plot without errors


if __name__ == "__main__":
    unittest.main()
