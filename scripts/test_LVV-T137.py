# Test script for LSST Data Management acceptance test campaign
# LVV-T137:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T137>
# LVV-T137 tests verification element LVV-130, <https://jira.lsstcorp.org/browse/LVV-130>
# which verifies requirement DMS-REQ-0299-V-01: Data Product Ingest
#
# The lsst environment must be set up to run this test,
# see <https://pipelines.lsst.io/install/setup.html> for more details

import os
import numpy as np
import astropy.units as u

from lsst.daf.butler import Butler

# Confirm the version of the Science Pipelines:
os.system('eups list -s | grep lsst_distrib')

repo = '/sdf/group/rubin/u/jcarlin/repos/rc2_subset/SMALL_HSC'
collection = 'u/jcarlin/step4'
butler = Butler(repo, collections=collection)

# DataId to select a single visit image:
dataId = {'instrument': 'HSC', 'detector': 42, 'visit': 19680}

calexp = butler.get('calexp', dataId=dataId)

# Check for a WCS, photocalib, image statistics, etc.
wcs = calexp.getWcs()

print('WCS for calexp image with dataId ', dataId, ':')
print(wcs)

pcalib = calexp.getPhotoCalib()

print('Photocalib for calexp image with dataId ', dataId, ':')
print(pcalib)

print('Image shape and statistics:')
print('Shape: ', np.shape(calexp.image.array))
print('Mean, median, std deviation of pixel values: ', np.nanmean(calexp.image.array), np.nanmedian(calexp.image.array), np.nanstd(calexp.image.array))

print('Variance plane shape and statistics:')
print('Shape: ', np.shape(calexp.variance.getArray()))
print('Mean, median, std deviation of pixel values: ', np.nanmean(calexp.variance.getArray()), np.nanmedian(calexp.variance.getArray()), np.nanstd(calexp.variance.getArray()))

print('Mask plane has the following mask bits set:')
print(calexp.mask.getMaskPlaneDict())

print('Mask plane has dimensions: ', calexp.mask.getDimensions())

# Check the source catalog:
src = butler.get('src', dataId=dataId)

print('Source catalog has ', len(src), ' entries.')

print('The first five entries in the source catalog:')
print(src[0:5])

print('The schema of the source catalog:')
print(src.getSchema())

psf_mags = pcalib.instFluxToMagnitude(src, 'base_PsfFlux')

print('Median of PSF magnitudes calculated using the associated PhotoCalib object:')
print(np.nanmedian(psf_mags[:,0]))
