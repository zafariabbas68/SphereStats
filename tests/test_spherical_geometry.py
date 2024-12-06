import unittest
import numpy as np
from SphereStats.sphere_stats import to_cartesian, haversine

class TestSphericalGeometry(unittest.TestCase):

    def test_to_cartesian(self):
        """Test the conversion of latitude/longitude to Cartesian coordinates."""
        lat, lon = 52.2296756, 21.0122287  # Warsaw
        # Expected Cartesian coordinates (6 decimals)
        expected = np.array([0.571769, 0.219622, 0.790472])
        result = to_cartesian(lat, lon)
        np.testing.assert_almost_equal(result, expected, decimal=6)  # Test with 6 decimals tolerance

    def test_haversine(self):
        """Test the Haversine formula to calculate distance."""
        lat1, lon1 = 52.2296756, 21.0122287  # Warsaw
        lat2, lon2 = 41.8919300, 12.5113300  # Rome
        expected_distance = 1315.510156  # Expected value with 6 decimals
        result = haversine(lat1, lon1, lat2, lon2)
        self.assertAlmostEqual(result, expected_distance, places=6)  # Compare to 6 decimal places

if __name__ == '__main__':
    unittest.main()
