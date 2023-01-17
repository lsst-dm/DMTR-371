# Test script for LSST Data Management acceptance test campaign
# LVV-T78:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T78>
# LVV-T78 tests verification element LVV-165, <https://jira.lsstcorp.org/browse/LVV-165>
# which verifies requirement DMS-REQ-0334-V-01: Persisting Data Products
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


def LVVT78(tract, patch, band):
    """ Execute test case LVV-T78 for best-seeing and deep coadd images

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
    print('\nInput dataId: ', dataId)

    try:
        goodseeing_coadd = butler.get('goodSeeingCoadd', **dataId)
        deep_coadd = butler.get('deepCoadd_calexp', **dataId)
    except:
        print('Invalid dataId. Please check and try again.')

    # Extract some statistics to confirm it is a well-formed image
    print('\nBest-seeing coadd image shape and statistics:')
    print('Shape: ', np.shape(goodseeing_coadd.image.array))
    print('Mean, median, std deviation of pixel values: ',
          np.nanmean(goodseeing_coadd.image.array),
          np.nanmedian(goodseeing_coadd.image.array),
          np.nanstd(goodseeing_coadd.image.array))
    print('\nDeep coadd image shape and statistics:')
    print('Shape: ', np.shape(deep_coadd.image.array))
    print('Mean, median, std deviation of pixel values: ',
          np.nanmean(deep_coadd.image.array),
          np.nanmedian(deep_coadd.image.array),
          np.nanstd(deep_coadd.image.array))

    # Examine the variance plane associated with the coadd:
    print('\nBest-seeing coadd variance plane shape and statistics:')
    print('Shape: ', np.shape(goodseeing_coadd.variance.getArray()))
    print('Mean, median, std deviation of pixel values: ',
          np.nanmean(goodseeing_coadd.variance.getArray()),
          np.nanmedian(goodseeing_coadd.variance.getArray()),
          np.nanstd(goodseeing_coadd.variance.getArray()))
    print('\nDeep coadd variance plane shape and statistics:')
    print('Shape: ', np.shape(deep_coadd.variance.getArray()))
    print('Mean, median, std deviation of pixel values: ',
          np.nanmean(deep_coadd.variance.getArray()),
          np.nanmedian(deep_coadd.variance.getArray()),
          np.nanstd(deep_coadd.variance.getArray()))

    # Examine the mask plane:
    print('Best-seeing coadd mask plane has dimensions: ', goodseeing_coadd.mask.getDimensions())
    print('Deep coadd mask plane has dimensions: ', deep_coadd.mask.getDimensions())

    # Check for a WCS and photocalib
    assert(deep_coadd.hasWcs())
    assert(goodseeing_coadd.hasWcs())
    print('Both images have a WCS.')

    assert(deep_coadd.hasPsf())
    assert(goodseeing_coadd.hasPsf())
    print('Both images have a PSF.')


if __name__ == "__main__":

    tract = 4431
    patch = 17
    bands = ['u', 'g', 'r', 'i', 'z', 'y']

    for band in bands:
        LVVT78(tract, patch, band)
