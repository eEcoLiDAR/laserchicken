# Point Cloud File Formats -work in progress
Handeling huge point clouds requires a spatial data structure to efficiatly access each point.
There is a multitude of File Formats that can be used with LAS and LAZ files. A summary of [File Formats](http://www.cloudcompare.org/doc/wiki/index.php?title=FILE_I/O), out of which we would focus on: 

* [CSV](https://docs.python.org/3/library/csv.html)

* PCD - the Point Cloud Library format [(PCL)](http://pointclouds.org/), python binding [NLeSc/python-pcl](https://github.com/NLeSC/python-pcl)

* PLY - Polygon File Format or the [Stanford Triangle Format](http://www.graphics.stanford.edu/data/3Dscanrep) 

* [Postgresql](https://www.postgresql.org/) - [NLeSc loader and quierier](https://github.com/NLeSC/pointcloud-benchmark/blob/master/python/pointcloud)


## PCD:
The [PCD](http://pointclouds.org/documentation/tutorials/pcd_file_format.php) file format is used as a file format to support 3D point cloud data. Please refer to [pointclouds.org](http://pointclouds.org/documentation/tutorials/pcd_file_format.php) for moe information and reference.
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
DATA - data type that the point cloud data is stored in: ascii/binary.```

