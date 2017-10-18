import os
import laspy
from plyfile import PlyData, PlyElement

def read_ply(inFile_path):
    '--------------------------'
    ' reads ply file using plyfile'
    '--------------------------'
    plydata = PlyData.read(inFile_path)
    x_att = plydata.elements[0].data['x']
    y_att = plydata.elements[0].data['y']
    z_att = plydata.elements[0].data['z']
    return x_att, y_att, z_att

def ply_2_las(x_att, y_att, z_att, las_header, OutFile_path):
    '--------------------------'
    ' writes  ply file format to LAS format using laspy'
    '--------------------------'
    #las_header = laspy.header.Header() #or = new_header
    outFile2 = laspy.file.File(OutFile_path, mode = "w", header = las_header)
    outFile2.X = x_att
    outFile2.Y = y_att    
    outFile2.Z = z_att
    outFile2.close()

