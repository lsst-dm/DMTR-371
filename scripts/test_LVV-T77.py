# Test script for LSST Data Management acceptance test campaign
# LVV-T77:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T77>
# LVV-T77 tests verification element LVV-161, <https://jira.lsstcorp.org/browse/LVV-161>
# which verifies requirement DMS-REQ-0330-V-01: Best Seeing Coadds
#
# The lsst environment must be set up to run this test,
# see <https://pipelines.lsst.io/install/setup.html> for more details

import os
import numpy as np
import astropy.units as u

from lsst.daf.butler import Butler

# Confirm the version of the Science Pipelines:
os.system('eups list -s | grep lsst_distrib')

# For DP0.2 data on the IDF:
config = 'dp02'
collection = '2.2i/runs/DP0.2'
butler = Butler(config, collections=collection)


def LVVT77(tract, patch, band):
    """ Execute test case LVV-T77 for best-seeing coadd images

    Parameters
    ----------
    tract: `int`
        Input tract for test
    patch: `int`
        Patch for which to extract image
    band: `str`
        Band for image to select
    """

    dataId = {'tract':tract, 'patch':patch, 'band':band}
    print('Input dataId: ', dataId)

    try:
        goodseeing_coadd = butler.get('goodSeeingCoadd', **dataId)
    except:
        print('Invalid dataId. Please check and try again.')

    # Extract some statistics to confirm it is a well-formed image
    print('\n Image shape and statistics:')
    print('Shape: ', np.shape(goodseeing_coadd.image.array))
    print('Mean, median, std deviation of pixel values: ',
          np.nanmean(goodseeing_coadd.image.array),
          np.nanmedian(goodseeing_coadd.image.array),
          np.nanstd(goodseeing_coadd.image.array))

    # Examine the variance plane associated with the coadd:
    print('\n Variance plane shape and statistics:')
    print('Shape: ', np.shape(goodseeing_coadd.variance.getArray()))
    print('Mean, median, std deviation of pixel values: ',
          np.nanmean(goodseeing_coadd.variance.getArray()),
          np.nanmedian(goodseeing_coadd.variance.getArray()),
          np.nanstd(goodseeing_coadd.variance.getArray()))

    # Examine the mask plane:
    print('\n Mask plane has the following mask bits set:')
    print(goodseeing_coadd.mask.getMaskPlaneDict())

    print('Mask plane has dimensions: ', goodseeing_coadd.mask.getDimensions())

    # Check for a WCS and photocalib
    wcs = goodseeing_coadd.getWcs()

    print('\n WCS for goodSeeingCoadd image with dataId ', dataId, ':')
    print(wcs)

    pcalib = goodseeing_coadd.getPhotoCalib()

    print('\n Photocalib for goodSeeingCoadd image with dataId ', dataId, ':')
    print(pcalib)

    # Extract the deep coadd and compare the PSF sizes of the
    # best-seeing and deep coadds.
    try:
        deep_coadd = butler.get('deepCoadd_calexp', **dataId)
    except:
        print('Invalid dataId. Please check and try again.')

    deep_coadd_psfradius = deep_coadd.getPsf().computeShape().getTraceRadius()
    goodseeing_coadd_psfradius = goodseeing_coadd.getPsf().computeShape().getTraceRadius()
    print('\n Good seeing coadd PSF radius: ', goodseeing_coadd_psfradius)
    print('Deep coadd PSF radius: ', deep_coadd_psfradius)


if __name__ == "__main__":

    tract = 4431
    patch = 17
    bands = ['u', 'g', 'r', 'i', 'z', 'y']

    for band in bands:
        LVVT77(tract, patch, band)
