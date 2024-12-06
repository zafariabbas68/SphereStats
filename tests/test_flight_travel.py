# test_flight_travel.py

import unittest
import numpy as np
import matplotlib.pyplot as plt
from SphereStats.flight_travel import haversine_distance, plot_flight_paths  # Adjust import path as necessary


class TestFlightTravel(unittest.TestCase):

    def test_haversine_distance(self):
        """
        Test the haversine distance function with known city pairs.
        """
        # Coordinates of New York and London for testing
        nyc = (40.7128, -74.0060)
        london = (51.5074, -0.1278)

        # Expected distance based on known values (around 5570 km)
        expected_distance = 5570.0

        # Calculate the distance using the haversine formula
        calculated_distance = haversine_distance(nyc[0], nyc[1], london[0], london[1])

        # Assert that the calculated distance is within a reasonable range
        self.assertAlmostEqual(calculated_distance, expected_distance, delta=50,
                               msg="Distance between NYC and London is incorrect.")

    def test_haversine_multiple_distances(self):
        """
        Test the haversine distance calculation for multiple city pairs.
        """
        # Coordinates for cities
        cities = {
            "New York": (40.7128, -74.0060),
            "London": (51.5074, -0.1278),
            "Dubai": (25.276987, 55.296249),
            "Tokyo": (35.6895, 139.6917),
            "Sydney": (-33.8688, 151.2093)
        }

        pairs = [
            ("New York", "London"),
            ("London", "Dubai"),
            ("Dubai", "Tokyo"),
            ("Tokyo", "Sydney"),
        ]

        for city1, city2 in pairs:
            lat1, lon1 = cities[city1]
            lat2, lon2 = cities[city2]
            calculated_distance = haversine_distance(lat1, lon1, lat2, lon2)
            self.assertGreater(calculated_distance, 0, msg=f"Distance between {city1} and {city2} is non-positive.")

    def test_plot_generation(self):
        """
        This test ensures that the plot for flight paths is generated.
        """
        try:
            plot_flight_paths()
        except Exception as e:
            self.fail(f"Plotting failed: {e}")


if __name__ == "__main__":
    unittest.main()
