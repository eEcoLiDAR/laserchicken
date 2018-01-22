import os
import numpy as np

from laserchicken import keys

def write(pc, path):
    # TODO: raise exception if file already exists?
    with open(path, 'w') as ply:
        write_header(pc,ply)
        write_data(pc,ply)

def write_header(pc,ply):
    ply.write("ply" + '\n')
    ply.write("format ascii 1.0" + '\n')
    write_comment(pc,ply)
    for elem_name in get_ordered_elems(pc.keys()):
        get_num_elems = (lambda d: len(d["x"].get("data",[]))) if elem_name == keys.point else None
        write_elements(pc,ply,elem_name,get_num_elems = get_num_elems)
    ply.write("end_header" + '\n')

def write_data(pc,ply):
    delim = ' '
    for elem_name in get_ordered_elems(pc.keys()):
        props = get_ordered_props(elem_name,pc[elem_name].keys())
        num_elems = len(pc[elem_name]["x"].get("data",[])) if elem_name == keys.point else 1
        for i in range(num_elems):
            for prop in props:
                datavalues = pc[elem_name][prop]["data"]
                if(isinstance(datavalues,np.ndarray)):
                    if(prop == props[-1]):
                        ply.write(formatply(datavalues[i]))
                    else:
                        ply.write(formatply(datavalues[i]) + delim)
                else:
                    if(i != 0):
                        raise Exception("Scalar quantity does not have element at index %d" % i)
                    ply.write(formatply(datavalues))
            ply.write('\n')


def formatply(obj):
    return str(obj)

def get_ordered_elems(elem_names):
    if(keys.point in elem_names):
        return [keys.point] + sorted([e for e in elem_names if e not in [keys.point,keys.provenance]])
    else:
        return sorted([e for e in elem_names if e not in [keys.point,keys.provenance]])


def get_ordered_props(elem_name,prop_list):
    if(elem_name == keys.point):
        return ['x','y','z'] + [k for k in sorted(prop_list) if k not in ['x','y','z']]
    else:
        return sorted(prop_list)

def write_comment(pc,ply):
    log = pc.get("log",[])
    if(any(log)):
        ply.write("comment [" + '\n')
        for msg in log:
            ply.write("comment " + str(msg) + '\n')
        ply.write("comment ]" + '\n')

def write_elements(pc,ply,elem_name,get_num_elems = None):
    if(elem_name in pc):
        num_elems = get_num_elems(pc[elem_name]) if get_num_elems else 1
        ply.write("element %s %d\n" % (elem_name,num_elems))
        keylist = get_ordered_props(elem_name,pc[elem_name].keys())
        for key in keylist:
            property_type = pc[elem_name][key]["type"]
            property_tuple = ("property",property_type,key)
            ply.write(" ".join(property_tuple) + '\n')
