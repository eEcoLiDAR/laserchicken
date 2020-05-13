# Spatial selection using the `filter` module

Filter is a module which provides functionality to run a range spatial selection over a set of points. The range should be specified as a **Polygon**, stored either in a WKT string or file, or in ESRI shapefile while points are defined as a *point_cloud* (**pc**).

## Two step spatial selection

Range selections are defined in two steps: filtering and refinement. The filtering step uses the polygon's bounding-box and the extent of the *point-cloud* to verify if they overlap. If they overlap, then in the refinement step **contains** from *shapely* is used to extract all points within the Polygon boundaries. 

## Examples

### Example with a WKT string.
```
from laserchicken import load
from laserchicken.filter import select_polygon

pc_in = load("testdata/AHN2.las")
wkt_string = "POLYGON(( 243590.0 572110.0, 243640.0 572160.0, 243700.0 572110.0, 243640.0 572060.0, 243590.0 572110.0 ))"
pc_out = select_polygon(pc_in, wkt_string)
```

### Example with a WKT file.
```
#At the moment only the first polygon will be used for the range selection.
from laserchicken import load
from laserchicken.filter import select_polygon

pc_in = load("testdata/AHN2.las")
filename = "testdata/ahn2_geometries_wkt/ahn2_polygon.wkt"
pc_out = select_polygon(pc_in, filename, read_from_file=True)
```

### Example with a ESRI shapefile.
```
#At the moment only the first polygon will be used for the range selection.
from laserchicken import load
from laserchicken.filter import select_polygon

pc_in = load("testdata/AHN2.las")
filename = "testdata/ahn2_geometries_shp/ahn2_polygon.shp"
pc_out = select_polygon(pc_in, filename, read_from_file=True)
```
