# Test script for LSST Data Management acceptance test campaign
# LVV-T129:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T129>
# LVV-T129 tests verification element LVV-18, <https://jira.lsstcorp.org/browse/LVV-18>
# which verifies requirement DMS-REQ-0043-V-01: Provide Calibrated Photometry
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


def LVVT129_src(instrument, visit, detector, cat_type, img_type):
    """ Execute test case LVV-T129 for single-visit PVI and
        difference images

    Parameters
    ----------
    instrument: `str`
        Instrument from which the data is derived
    visit: `int`
        Input visit for test
    detector: `int`
        Detector on which to test schema
    cat_type: `str`
        Type of input catalog on which to test; either "src"
        or "goodSeeingDiff_diaSrc" (or anything with dimensions
        of visit, detector that also contains PSF fluxes)
    img_type: `str`
        Type of image to extract photocalib from for calibration
    """

    dataId = {'instrument':instrument, 'visit':visit, 'detector':detector}
    print('Input dataId: ', dataId)

    try:
        src = butler.get(cat_type, dataId = dataId)
        pcalib = butler.get(img_type, dataId = dataId).getPhotoCalib()

    except:
        print('Invalid dataId. Please check and try again.')

    src_flux_njy0 = pcalib.instFluxToNanojansky(src, 'base_PsfFlux')
    src_mag0 = pcalib.instFluxToMagnitude(src, 'base_PsfFlux')

    # Keep only positive fluxes
    keep = (src_flux_njy0[:,0] > 0)
    src_flux_njy = src_flux_njy0[keep, 0]
    src_mag = src_mag0[keep, 0]

    converted_fluxes = []

    for i in range(len(src_flux_njy)):
        tmp_mag = pcalib.instFluxToMagnitude(src_flux_njy[i])
        converted_fluxes.append(tmp_mag)

    converted_fluxes = np.array(converted_fluxes)

    # Compare mags from photocalib to mags converted from flux via astropy tools;
    fff = src_flux_njy*u.nJy
    
    if np.allclose(src_mag, fff.to(u.ABmag).value, equal_nan=True):
        # If nJy fluxes and ABmags are available, print this message.
        print('\n TRUE: '+cat_type+' table fluxes are available in calibrated nJy and ABmag.')
    else:
        print('\n FALSE: converted fluxes not equal.')


if __name__ == "__main__":

    # Select an arbitrary source catalog from a PVI and difference image:
    instrument = 'LSSTCam-imSim'
    detector = 5
    visit = 924041
    src_cat = 'src'
    pvi_img = 'calexp'
    dia_src_cat = 'goodSeeingDiff_diaSrc'
    diff_img = 'goodSeeingDiff_differenceExp'

    # Run the test for the "src" catalog:
    LVVT129_src(instrument, visit, detector, src_cat, pvi_img)

    # Run the test for the "DIASrc" catalog:
    LVVT129_src(instrument, visit, detector, dia_src_cat, diff_img)
