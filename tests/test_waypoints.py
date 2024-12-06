import unittest
from SphereStats.waypoints import (
    to_cartesian,
    haversine_distance,
    interpolate_waypoints,
    total_travel_distance,
    plot_waypoints
)

class TestWaypoints(unittest.TestCase):
    def setUp(self):
        self.start = (40.7128, -74.0060)  # New York City
        self.end = (48.8566, 2.3522)      # Paris
        self.waypoints = interpolate_waypoints(self.start, self.end, num_points=5)

    def test_to_cartesian(self):
        cartesian = to_cartesian(40.7128, -74.0060)
        self.assertEqual(len(cartesian), 3)

    def test_haversine_distance(self):
        distance = haversine_distance(self.start, self.end)
        self.assertAlmostEqual(distance, 5837, delta=50)  # Approximate great-circle distance

    def test_interpolate_waypoints(self):
        self.assertEqual(len(self.waypoints), 5)
        self.assertAlmostEqual(self.waypoints[0][0], self.start[0], delta=0.5)
        self.assertAlmostEqual(self.waypoints[-1][0], self.end[0], delta=0.5)

    def test_total_travel_distance(self):
        waypoints_for_route = [self.start] + self.waypoints + [self.end]
        total_distance = total_travel_distance(waypoints_for_route)
        self.assertGreater(total_distance, 0)
        self.assertAlmostEqual(total_distance, 5837, delta=50)

    def test_plot_waypoints(self):
        """
        Verify that plot_waypoints runs without errors.
        """
        try:
            plot_waypoints(self.start, self.end, self.waypoints)
        except Exception as e:
            self.fail(f"plot_waypoints raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
