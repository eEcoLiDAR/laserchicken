import numpy as np
import scipy.stats.stats as stats

from laserchicken.feature_extractor.abc import AbstractFeatureExtractor
from laserchicken.keys import point

class PercentileFeatureExtractor(AbstractFeatureExtractor):
	'''
	Compute the height percentile of the pc
	'''
	@classmethod
	def requires(cls):
		return []

	@classmethod
	def provides(cls):
		return ['perc_'+str(i) for i in range(10,110,10)]

	def extract(self,sourcepc,neighborhood,targetpc,targetindex):
		z = sourcepc[point]['z']['data'][neighborhood]
		percentiles = range(10,110,10)
		return [stats.scoreatpercentile(z,p) for p in percentiles]