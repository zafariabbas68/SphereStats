import unittest
import numpy as np
import matplotlib.pyplot as plt
from SphereStats.convex_hull import spherical_to_cartesian, convex_hull_on_sphere, plot_convex_hull_3d, \
    plot_convex_hull_2d  # Importing functions from SphereStats


class TestConvexHull(unittest.TestCase):

    def setUp(self):
        # Define random points on a sphere (latitude, longitude in degrees)
        self.points = np.array([
            [40.748817, -73.985428],  # New York
            [34.052235, -118.243683],  # Los Angeles
            [48.8566, 2.3522],  # Paris
            [-33.8688, 151.2093],  # Sydney
            [35.6895, 139.6917],  # Tokyo
            [51.5074, -0.1278],  # London
            [-23.5505, -46.6333],  # São Paulo
            [55.7558, 37.6173],  # Moscow
        ])

    def test_convex_hull_on_sphere(self):
        # Compute convex hull
        hull, cartesian_points = convex_hull_on_sphere(self.points)

        # Test that convex hull was computed successfully (hull should not be empty)
        self.assertIsNotNone(hull)
        self.assertGreater(len(hull.vertices), 0)

    def test_plot_convex_hull_3d(self):
        try:
            # Compute convex hull
            hull, cartesian_points = convex_hull_on_sphere(self.points)

            # Plot the convex hull in 3D
            plot_convex_hull_3d(hull, cartesian_points)

            # Close the plot after test
            plt.close()

        except Exception as e:
            self.fail(f"plot_convex_hull_3d raised an exception: {e}")

    def test_plot_convex_hull_2d(self):
        try:
            # Compute convex hull
            hull, cartesian_points = convex_hull_on_sphere(self.points)

            # Plot the convex hull in 2D
            plot_convex_hull_2d(self.points, hull)

        except Exception as e:
            self.fail(f"plot_convex_hull_2d raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
