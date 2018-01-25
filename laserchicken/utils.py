import numpy as np
import datetime
from laserchicken import keys,_version

def get_point(pc,index):
    return pc[keys.point]["x"]["data"][index],pc[keys.point]["y"]["data"][index],pc[keys.point]["z"]["data"][index]


def get_feature(pc,index,featurename):
    return pc[keys.point][featurename]["data"][index]


def get_features(pc,index,featurenames):
    return (pc[keys.point][f]["data"][index] for f in featurenames)


def copy_pointcloud(pc_in, array_mask = None):
    """
    Makes a deep copy of a point cloud dict using the array mask when copying the points.
    :param pc_in: Input point cloud
    :param array_mask: A mask indicating which points to copy.
    :return: The copy including only the masked points.
    """
    result = {}
    for key, value in pc_in.items():
        if isinstance(value, dict):
            new_value = copy_pointcloud(value, array_mask)
        elif isinstance(value, np.ndarray):
            if array_mask is not None:
                new_value = value[array_mask] if any(value) else np.copy(value)
            else:
                new_value = np.copy(value)
        else:
            new_value = value
        result[key] = new_value
    return result


def add_metadata(pc,module,params):
    """
    Adds module metadata to pointcloud provenance
    """
    msg = {"time" : datetime.datetime.utcnow()}
    msg["module"] = module.__name__ if hasattr(module,"__name__") else str(module)
    if(any(params)): msg["parameters"] = params
    msg["version"] = _version.__version__
    if(keys.provenance not in pc):
        pc[keys.provenance] = []
    pc[keys.provenance].append(msg)
