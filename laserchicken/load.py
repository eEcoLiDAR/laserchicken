from laserchicken import read_las
from laserchicken import write_ply


def load(input_las_path, output_ply_path):
    pc = read_las.read(input_las_path)
    write_ply.write(pc, output_ply_path)
