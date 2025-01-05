
import unittest
from SphereStats.isochrone_travel import haversine_distance, generate_isochrones, plot_isochrones  # Corrected module name


class TestIsochroneTravel(unittest.TestCase):

    def test_haversine_distance(self):
        # Test known distances between pairs of coordinates
        nyc = (40.7128, -74.0060)  # New York
        london = (51.5074, -0.1278)  # London

        expected_distance = 5570.0  # Known distance between NYC and London (in km)
        calculated_distance = haversine_distance(nyc[0], nyc[1], london[0], london[1])

        # Assert that the calculated distance is correct
        self.assertAlmostEqual(calculated_distance, expected_distance, delta=50, msg="Distance is incorrect.")

    def test_generate_isochrones(self):
        center_lat, center_lon = 40.7128, -74.0060  # New York City coordinates
        time_thresholds = [1, 2, 3]

        isochrones = generate_isochrones(center_lat, center_lon, time_thresholds)

        # Ensure that the isochrones list contains 3 isochrones
        self.assertEqual(len(isochrones), 3, "There should be 3 isochrones.")

    def test_plot_generation(self):
        try:
            plot_isochrones()  # This will generate and display the plot
        except Exception as e:
            self.fail(f"Plotting failed: {e}")

if __name__ == "__main__":
    unittest.main()



