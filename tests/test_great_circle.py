# test_great_circle.py

import unittest
import numpy as np
import matplotlib.pyplot as plt
from SphereStats.great_circle import great_circle_arc, \
    plot_great_circle_arcs  # Modify import path as per your library structure


class TestGreatCircleArc(unittest.TestCase):

    def test_great_circle_arc(self):
        # Coordinates of New York and Paris for a known arc
        nyc = (40.7128, -74.0060)
        paris = (48.8566, 2.3522)

        # Calculate the arc
        arc_lat, arc_lon = great_circle_arc(nyc[0], nyc[1], paris[0], paris[1])

        # Check if the calculated latitudes and longitudes are not empty
        self.assertGreater(len(arc_lat), 0, "Latitude points should not be empty.")
        self.assertGreater(len(arc_lon), 0, "Longitude points should not be empty.")

        # Check if the arc returns correct number of points
        self.assertEqual(len(arc_lat), 100, "Should return 100 points by default.")

        # Optionally, test for a specific point on the arc, e.g., first point
        self.assertAlmostEqual(arc_lat[0], nyc[0], delta=0.1,
                               msg="First latitude should be close to New York's latitude.")
        self.assertAlmostEqual(arc_lon[0], nyc[1], delta=0.1,
                               msg="First longitude should be close to New York's longitude.")

        # Test the last point (should be close to Paris)
        self.assertAlmostEqual(arc_lat[-1], paris[0], delta=0.1,
                               msg="Last latitude should be close to Paris' latitude.")
        self.assertAlmostEqual(arc_lon[-1], paris[1], delta=0.1,
                               msg="Last longitude should be close to Paris' longitude.")

    def test_great_circle_multiple_points(self):
        # Coordinates of New York and Tokyo for a known arc
        nyc = (40.7128, -74.0060)
        tokyo = (35.6895, 139.6917)

        # Calculate the arc
        arc_lat, arc_lon = great_circle_arc(nyc[0], nyc[1], tokyo[0], tokyo[1])

        # Check if the calculated latitudes and longitudes are not empty
        self.assertGreater(len(arc_lat), 0, "Latitude points should not be empty.")
        self.assertGreater(len(arc_lon), 0, "Longitude points should not be empty.")

        # Verify if the function works for multiple points
        self.assertEqual(len(arc_lat), 100, "Should return 100 points by default.")

    def test_plot_generation(self):
        """
        This test ensures that the plot for great-circle arcs is generated.
        """
        # Run the plot function (this will generate and display the plot)
        try:
            plot_great_circle_arcs()
        except Exception as e:
            self.fail(f"Plotting failed: {e}")


if __name__ == "__main__":
    unittest.main()
