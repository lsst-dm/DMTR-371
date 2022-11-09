# Test script for LSST Data Management acceptance test campaign
# LVV-T32:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T32>
# LVV-T32 tests verification element LVV-11, <https://jira.lsstcorp.org/browse/LVV-11>
# which verifies requirement DMS-REQ-0024-V-01: Raw Image Assembly
#
# The lsst environment must be set up to run this test,
# see <https://pipelines.lsst.io/install/setup.html> for more details

import os
import numpy as np
import astropy.units as u

from lsst.daf.butler import Butler

# Confirm the version of the Science Pipelines:
os.system('eups list -s | grep lsst_distrib')

repo = '/repo/embargo'
collection = 'u/huanlin/auxtel_oga_panda_test_2022102528_w44'
butler = Butler(repo, collections=collection)

# DataId to select a single visit image:
dataId = {'exposure':2022092900894, 'detector':0}

raw = butler.get('raw', dataId=dataId)

# Check for a WCS, photocalib, image statistics, etc.
print('\nWhat type of object is it?')
print(raw)

print('\nPixel data type:')
print(raw.dtype)

print('\nVisit info: ')
print(raw.visitInfo)

print('\nImage shape and statistics:')
print('Shape: ', np.shape(raw.image.array))
print('Mean, median, std deviation of pixel values: ', np.nanmean(raw.image.array),
      np.nanmedian(raw.image.array), np.nanstd(raw.image.array))

print('\nMetadata: ')
md = raw.getMetadata()
md_dict = md.toDict()

for item in md_dict.items():
    print(item)

