import inspect

import laserchicken
from laserchicken.volume_specification import Volume


def create_volume_map():
    """ Generate map of volume types that are available """
    volume_map = {}
    for name, obj in inspect.getmembers(laserchicken.volume_specification):
        if inspect.isclass(obj) and issubclass(obj, Volume) and obj is not Volume:
            volume_map[obj.TYPE] = obj
    return volume_map


VOLUMES = create_volume_map()


def build_volume(volume_type, *args, **kwargs):
    """
    Return volume object from the volume name and the corresponding parameters

    Example:
    >>>> vol = build_volume('sphere', radius=5)

    :param volume_type: name corresponding to the
    :param args: optional non-keyword args to build the volume
    :param kwargs: optional keyword args to build the volume
    :return:
    """
    _volume_type = volume_type.lower()
    _verify_volume_type(_volume_type)
    volume_builder = VOLUMES[_volume_type]
    return volume_builder(*args, **kwargs)


def _verify_volume_type(volume_type):
    if volume_type not in VOLUMES.keys():
        raise ValueError('Unknown volume specified: {}. Available volumes are: {}'
                         .format(volume_type, ', '.join(VOLUMES.keys())))
