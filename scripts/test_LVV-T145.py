# Test script for LSST Data Management acceptance test campaign
# LVV-T145:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T145>
# LVV-T145 tests verification element LVV-137, <https://jira.lsstcorp.org/browse/LVV-137>
# which verifies requirement DMS-REQ-0306-V-01: Task Configuration
#
# The lsst environment must be set up to run this test,
# see <https://pipelines.lsst.io/install/setup.html> for more details

import os
import numpy as np

from lsst.daf.butler import Butler

# Confirm the version of the Science Pipelines:
os.system('eups list -s | grep lsst_distrib')

# Initialize the butler separately with each collection:
butler = Butler('/sdf/home/j/jcarlin/u/repos/rc2_subset/SMALL_HSC/',
                collections=['u/jcarlin/LVV-T145_step1_thresh100'])
butler2 = Butler('/sdf/home/j/jcarlin/u/repos/rc2_subset/SMALL_HSC/',
                 collections=['u/jcarlin/LVV-T145_step1_thresh30'])

# Pick a single visit/detector:
dataId1 = {'visit':11690, 'detector':42, 'instrument':'HSC'}

# Extract the source tables for the two runs:
src1 = butler.get('src', dataId1)
src2 = butler2.get('src', dataId1)

# Print the length of the source tables:
print('src1 length: ', len(src1))
print('src2 length: ', len(src2))

# Extract the configs for each run
cfg1 = butler.get('characterizeImage_config', dataId1).toDict()
cfg2 = butler2.get('characterizeImage_config', dataId1).toDict()

# Print the detection.thresholdValue, since that’s what we changed between the two configs:
print('run1 threshold: ', cfg1['detection']['thresholdValue'])
print('run2 threshold: ', cfg2['detection']['thresholdValue'])

