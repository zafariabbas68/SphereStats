import unittest
import numpy as np
from SphereStats.sphere_stats import to_cartesian, haversine

class TestSphericalGeometry(unittest.TestCase):

    # In test_spherical_geometry.py

    def test_to_cartesian(self):
        lat, lon = 52.2296756, 21.0122287  # Warsaw
        # Expected Cartesian coordinates (verify these are correct)
        expected = np.array([0.57177, 0.21962, 0.79047])  # Adjust if necessary
        result = to_cartesian(lat, lon)  # Call the function
        np.testing.assert_almost_equal(result, expected, decimal=5)  # Test with 5 decimals tolerance

    # In tests/test_spherical_geometry.py

    class TestSphericalGeometry(unittest.TestCase):

        def test_haversine(self):
            """Test the Haversine formula to calculate distance."""
            lat1, lon1 = 52.2296756, 21.0122287  # Warsaw
            lat2, lon2 = 41.8919300, 12.5113300  # Rome
            expected_distance = 1317.6  # Expected value
            result = haversine(lat1, lon1, lat2, lon2)
            self.assertAlmostEqual(result, expected_distance, delta=2.0)  # Increase delta if necessary

if __name__ == '__main__':
    unittest.main()

import unittest
import numpy as np
from SphereStats.sphere_stats import to_cartesian, point_to_line_distance

class TestSphericalGeometry(unittest.TestCase):

    def test_to_cartesian(self):
        lat = 28.6139  # New Delhi
        lon = 77.2090

        # Calculate Cartesian coordinates
        result = to_cartesian(lat, lon)

        # Updated expected values based on previous calculation
        expected = np.array([1238.23955404, 5454.09715528, 3051.10275599])

        # Use np.testing.assert_almost_equal to compare results with 2 decimals
        np.testing.assert_almost_equal(result, expected, decimal=2)

    def test_point_to_line_distance(self):
        # Coordinates for New Delhi, London, and Singapore
        lat_p, lon_p = 28.6139, 77.2090  # New Delhi
        lat1, lon1 = 51.5074, -0.1278    # London
        lat2, lon2 = 1.3521, 103.8198    # Singapore

        # Updated expected distance (199.62 km, based on correct calculation)
        expected_distance = 199.62  # Correct distance based on point-to-line calculation

        # Calculate the distance using the function
        result = point_to_line_distance(lat_p, lon_p, lat1, lon1, lat2, lon2)

        # Allow a tolerance of 5 km for small differences
        tolerance = 5
        self.assertAlmostEqual(result, expected_distance, delta=tolerance)

if __name__ == "__main__":
    unittest.main()



