SphereStats is a Python library I developed for geospatial analysis and geodesic calculations. It provides efficient tools for computing distances, generating isochrones, and performing other geospatial operations. Built using popular libraries like geopandas, pyproj, and shapely, SphereStats simplifies working with geographic data, projections, and geometric computations.
The library is designed to assist in tasks such as:
* Calculating distances between points using the Haversine and geodesic formulas
* Generating isochrones for travel-time analysis
* Visualizing spatial data with matplotlib
* Performing spatial operations with geopandas and shapely
SphereStats is aimed at researchers, data analysts, and developers working in geospatial, environmental, or transportation fields, providing an easy-to-use toolset for handling geographic data and analyses.

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
