# Spatial selection

Spatial selection is a module which provides functionality to run a range spatial selection over a set of points. The range should be specified as a **Polygon**, stored either in a WKT string or file, or in ESRI shapefile while points are defined as a *point_cloud* (**pc**).

## Two step Spatial selection

Range selections are defined in two steps: filtering and refinement. The filtering step uses the polygon's bounding-box and the extent of the *point-cloud* to verify if they overlap. If they overlap, then in the refinement step **contains** from *shapely* is used to extract all points within the Polygon boundaries. 

## Examples

### Example with a WKT string.
```
from laserchicken.keys import point
from laserchicken import read_las
from laserchicken.spatial_selections import points_in_polygon_wkt

pc_in = read_las.read("laserchicken/testdata/AHN2.las")
pc_out = points_in_polygon_wkt(pc_in, "POLYGON(( 243590.0 572110.0, 243640.0 572160.0, 243700.0 572110.0, 243640.0 572060.0, 243590.0 572110.0 ))")
```

### Example with a WKT file.
```
#At the moment only the first polygon will be used for the range selection.
from laserchicken.keys import point
from laserchicken import read_las
from laserchicken.spatial_selections import points_in_polygon_wkt_file

pc_in = read_las.read("laserchicken/testdata/AHN2.las")
pc_out = points_in_polygon_wkt_file(pc_in, "laserchicken/testdata/anh2_geometries_wkt/ahn2_polygon.wkt")
```

### Example with a ESRI shapefile.
```
#At the moment only the first polygon will be used for the range selection.
from laserchicken.keys import point
from laserchicken import read_las
from laserchicken.spatial_selections import points_in_polygon_shp_file

pc_in = read_las.read("laserchicken/testdata/AHN2.las")
pc_out = points_in_polygon_shp_file(pc_in, "laserchicken/testdata/anh2_geometries_shp/ahn2_polygon.shp")
```

## Future work
The *refinement* step could be further improved if the points were indexed with a *Kd-tree* or a grid index. Such approache would avoid to execution of **contains** for all the points.
