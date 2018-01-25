import numpy as np
from laserchicken import keys
from laserchicken.feature_extractor.abc import AbstractFeatureExtractor

class EntropyFeatureExtractor(AbstractFeatureExtractor):

    # TODO: make this settable from command line
    layer_thickness = 0.5
    zmin = None
    zmax = None

    @classmethod
    def requires(cls):
        return []

    @classmethod
    def provides(cls):
        return ['z_entropy']

    def get_params(self):
        p = [self.layer_thickness]
        if(not self.zmin is None):
            p.append(self.zmin)
        if(not self.zmax is None):
            p.append(self.zmax)
        return p


    def extract(self,sourcepc,neighborhood,targetpc,targetindex):
        z = sourcepc[keys.point]["z"]["data"][neighborhood]
        _zmin = np.min(z) if self.zmin is None else self.zmin
        _zmax = np.max(z) if self.zmax is None else self.zmax
        nbins = int(np.ceil((_zmax - _zmin)/self.layer_thickness))
        data = np.histogram(z,bins = nbins,range = (_zmin,_zmax),density = True)[0]
        entropyfunc = np.vectorize(xlog2x)
        norm = np.sum(data)
        return -(entropyfunc(data/norm)).sum()


def xlog2x(x):
    return 0 if x == 0 else x * np.log2(x)
