SphereStats

SphereStats is a Python library designed for advanced geospatial analysis and spherical geometry operations. Whether you're working with geographic data, analyzing navigation routes, or performing spatial statistics, SphereStats provides the tools you need to simplify and streamline the workflows.

 Key Features

1. Distance Calculations:
	Great-circle distance using the Haversine formula.
	Point-to-line and point-to-polygon distances for geofencing and proximity analysis.
	Midpoint calculations for navigation and routing.
   
2. Routing and Network Analysis:
	Compute the shortest paths between points on a sphere.
	Generate waypoints along routes for navigation or migration tracking.
	Calculate travel distances along curved paths, such as roads or flight paths.

3. Geometric and Statistical Analysis:
	Centroid and bounding circle calculations for multiple points on a sphere.
	Convex hull computations for clustering and spatial extents.
	Create Voronoi diagrams for resource allocation and coverage analysis.
	Cluster points based on distance thresholds or other metrics.

4. Proximity Analysis:
	Generate buffer zones around points, lines, or polygons.
	Find nearest neighbors or K-nearest neighbors for a given point.
	Perform distance threshold queries for proximity-based operations.


5. Visualization:
	Render routes, heatmaps, and geometric shapes on various map projections.
	Visualize great-circle arcs and spherical triangles for navigation and celestial mapping.

6. Advanced Metrics:
	Spherical triangle calculations for navigation.
	Weighted distances incorporating terrain difficulty or travel speeds.
	Isochrone maps showing areas reachable within time thresholds.

Installation

Install SphereStats using pip:

bash
pip install SphereStats

 Example Usage

from SphereStats.convex_hull import convex_hull_on_sphere, plot_convex_hull_3d

# Define latitude and longitude points
points = [
    [40.748817, -73.985428],  # New York
    [34.052235, -118.243683],  # Los Angeles
    [48.8566, 2.3522],  # Paris
    [-33.8688, 151.2093],  # Sydney
    [35.6895, 139.6917],  # Tokyo
]

# Compute the convex hull
hull, cartesian_points = convex_hull_on_sphere(points)

# Visualize in 3D
plot_convex_hull_3d(hull, cartesian_points)

Applications

	Navigation and Routing:
	Calculate optimal routes and travel paths.
	Analyze waypoint-based navigation for flights and shipping.
	Geospatial Analysis:
	Assess proximity to protected areas, hazard zones, or geofences.
	Perform clustering and resource allocation using spherical statistics.
	Data Visualization:
	Generate intuitive maps and spherical projections for spatial data.
	Urban Planning and Infrastructure:
	Plan routes, assess coverage zones, and analyze accessibility.
  
Requirements

   Python >= 3.8
   Required packages:
      - numpy
      - scipy
      - matplotlib
      - cartopy
      - pyproj

 Contributing

Contributions are welcome! If you have suggestions, bug reports, or feature requests, feel free to submit an issue or pull request on the [GitHub repository[(https://github.com/zafariabbas68/SphereStats).

License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.




# usage example
from SphereStats.flight_travel import haversine_distance, plot_flight_paths                                                                                                           
from SphereStats.isochrone_travel import haversine_distance, generate_isochrones, plot_isochrones

from SphereStats.network_routing import (
    to_cartesian,
    haversine_distance,
    dijkstra,
    create_network,
    plot_network,
    plot_routes 
    )
