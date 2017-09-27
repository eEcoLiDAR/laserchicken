# Point Cloud File Formats -work in progress
Handeling huge point clouds requires a spatial data structure to efficiatly access each point.
There is a multitude of File Formats that can be used with LAS and LAZ files. A summary of [File Formats](http://www.cloudcompare.org/doc/wiki/index.php?title=FILE_I/O), out of which we would focus on: 

* [CSV](https://docs.python.org/3/library/csv.html)

* PCD - the Point Cloud Library format [(PCL)](http://pointclouds.org/), python binding [NLeSc/python-pcl](https://github.com/NLeSC/python-pcl)

* PLY - Polygon File Format or the [Stanford Triangle Format](http://www.graphics.stanford.edu/data/3Dscanrep) 

* [Postgresql](https://www.postgresql.org/) - [NLeSc loader and quierier](https://github.com/NLeSC/pointcloud-benchmark/blob/master/python/pointcloud)


## PCD:
The [PCD](http://pointclouds.org/documentation/tutorials/pcd_file_format.php) is used as a file format to support 3D point cloud data. Please refer to [pointclouds.org](http://pointclouds.org/documentation/tutorials/pcd_file_format.php) for reference and more information.
Each PCD file contains a header (ASCII) that identifies and declares certain properties of the point cloud data stored in the file. 

**HEADER:** The header entries must be specified precisely in the following order:
```
VERSION - PCD file version
FIELDS -  name of each dimension/field that a point can have, for example: xyz, rgb (colors), surface normals, moment invariants (j1-3) and more...
* FIELDS x y z                                
* FIELDS x y z rgb                            
* FIELDS x y z normal_x normal_y normal_z     
* FIELDS j1 j2 j3                             
SIZE - size of each dimension in bytes
TYPE - type of each dimension as a char.
* I - represents signed types int8 (char), int16 (short), and int32 (int)
* U - represents unsigned types uint8 (unsigned char), uint16 (unsigned short), uint3(unsigned int)
* F - represents float types
COUNT - specifies how many elements does each dimension have. For example, x data usually has 1 element, but a feature descriptor like the VFH has 308. Basically this is a way to introduce n-D histogram descriptors at each point, and treating them as a single contiguous block of memory. Default: count=1.
WIDTH - width of the point cloud dataset in the number of points, one of the 2 meanings: 
* total number of points in the cloud (equal with POINTS see below) for unorganized datasets
* total number of points in a row of an organized point cloud dataset.
HEIGHT - height of the point cloud dataset in the number of points, one of the 2 meanings:
* HEIGHT=1 for unorganized datasets (thus used to check whether a dataset is organized or not).
* specify the height (total number of rows) of an organized point cloud dataset
VIEWPOINT - specifies an acquisition viewpoint for the points in the dataset. The viewpoint information is specified as a translation (tx ty tz) + quaternion (qw qx qy qz). Default: VIEWPOINT 0 0 0 1 0 0 0
POINTS - total number of points in the cloud. 
DATA - data type that the point cloud data is stored in: ascii/binary.
```
**Attributes**

PCL comes with a variety of pre-defined point types, ranging from SSE-aligned structures for XYZ data, to more complex n-dimensional histogram representations such as PFH (Point Feature Histograms). 
A list of all the [PCD pre-defined point types](https://github.com/PointCloudLibrary/pcl/blob/master/common/include/pcl/impl/point_types.hpp).


* You can [add custom point type](http://pointclouds.org/documentation/tutorials/adding_custom_ptype.php) to the point cloud.

## PLY:
Format for storing graphical objects that are described as a collection of polygons. 
PLY is composed of an header followed by a list of vertices and  a list of polygons. The header specifies how many vertices and polygons are in the file, and also states what properties are associated with each vertex, such as (x,y,z) coordinates, normals and color. The polygon faces are simply lists of indices into the vertex list, and each face begins with a count of the number of elements in each list. 

Please refer to [paulbourke- PLY file format](http://paulbourke.net/dataformats/ply/) for reference and more information.

**HEADER**: A sample header must follow this specification: 
```
ply
format ascii 1.0
comment Mars model by Paul Bourke
element vertex 259200
property float x
property float y
property float z
element face 516960
property list uchar int vertex_indices
end_header
```

* ply - file format
* format - ascii 1.0, binary_little_endian 1.0, binary_big_endian 1.0
* comment - a comment which is ignored
* element - a description of how some particular data element is stored and how many of them there are. 
In a file where there are 12 vertices, each represented as a floating point (X,Y,Z) triple, one would expect to see:
```
element vertex 12
property float x
property float y
property float z
```
Other properties may indicate colours or other data items are stored at each vertex and indicate the data type of that information. Data types can be one of two variants, depending on the source of the ply file. The type can be specified with one of char uchar short ushort int uint float double, or one of int8 uint8 int16 uint16 int32 uint32 float32 float64.

At the end of the header, there must always be the line:
```
end_header
```

**Attributes**

A variety of properties can be stored, including: xyz, color, surface normals, texture coordinates and data confidence values.

The structure of a typical PLY file:
```
  Header
  Vertex List
  Face List
  (lists of other elements)
```
* Adding new attributes - applications can create new properties that are attached to elements of an object. The format for defining a new element is exactly the same as for vertices, faces and edges. 

**Log**

A log or comments can be placed in the header by using the word comment at the start of the line. Everything from there until the end of the line is ignored.
```
  comment this is ignored
```
A sample file addapted from [paulbourke](http://paulbourke.net/dataformats/ply/example1.ply):

```
ply
format ascii 1.0
comment Mars model by Paul Bourke
element vertex 259200
property float x
property float y
property float z
element face 516960
property list uchar int vertex_indices
end_header
15081.5 -3.45644e+06 65.8061
15081 -3.45659e+06 197.422
15078.2 -3.45648e+06 329.009
15075.4 -3.45663e+06 460.597
15071.2 -3.4567e+06 592.148
15065.6 -3.45674e+06 723.653
15059.9 -3.457e+06 855.16
15050.7 -3.45674e+06 986.473

     lots of vertices follow

14541.2 3.33642e+06 -698.464
14547.7 3.33663e+06 -571.58
14551.5 3.33649e+06 -444.589
14552.7 3.336e+06 -317.541
14556.9 3.33645e+06 -190.56
14558.7 3.33661e+06 -63.5247
3 0 721 1
3 721 0 720
3 1 722 2
3 722 1 721
3 2 723 3
3 723 2 722

     lots of triangular facets follow
```

