import laspy


def write(pc, path):
    header = laspy.header.Header()
    out_file = laspy.file.File(path, mode="w", header=header)
    out_file.X = pc['points']['x']['data']
    out_file.Y = pc['points']['y']['data']
    out_file.Z = pc['points']['z']['data']
    out_file.close()
