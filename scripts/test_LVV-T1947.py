# Test script for LSST Data Management acceptance test campaign
# LVV-T1947:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T1947>
# LVV-T1947 tests verification element LVV-178, <https://jira.lsstcorp.org/browse/LVV-178>
# which verifies requirement DMS-REQ-0347-V-01: Measurements in catalogs
#
# The lsst environment must be set up to run this test,
# see <https://pipelines.lsst.io/install/setup.html> for more details

import os
import numpy as np

from lsst.daf.butler import Butler

# Confirm the version of the Science Pipelines:
os.system('eups list -s | grep lsst_distrib')

# For DP0.2 data on the IDF:
config = 'dp02'
collection = '2.2i/runs/DP0.2'
butler = Butler(config, collections=collection)

def LVVT1947(instrument, visit, detector):
    """ Execute test case LVV-T1947

    Parameters
    ----------
    instrument: `str`
        Instrument from which the data is derived
    visit: `int`
        Input visit for test
    detector: `int`
        Detector on which to test schema
    """

    dataId = {'instrument':instrument, 'visit':visit, 'detector':detector}
    print('Input dataId: ', dataId)

    try:
        src = butler.get('goodSeeingDiff_diaSrc', dataId = dataId)
    except:
        print('Invalid dataId. Please check and try again.')

    sch = src.schema
    src_flag = check_schema(sch)

    # If any of the units are not "count," print "FALSE."
    assert(np.all(src_flag)), 'FALSE: not all instFlux entries have units of counts.'
    
    # If all of the flux units are "count," print "TRUE."
    print('\n All diaSrc table instFlux entries have units of counts: ', np.all(src_flag))


def check_schema(sch):
    """ Check the units on each flux entry in the schema

    Parameters
    ----------
    sch: Schema 
        src catalog schema to check

    Returns
    -------
    src_flag: `list` of `bool`
        Boolean list containing "True" for elements with flux units in "count"
    """

    src_flag = []
    for entry in sch:
        field = entry.getField().getName()
        if 'instFlux' in field and 'flag' not in field and 'Cov' not in field:
            flux_units = entry.getField().getUnits()
            src_flag.append('count' in flux_units)
            print(f'{field:60}..... {flux_units:20}')
    return src_flag


if __name__ == "__main__":

    # Select an arbitrary source catalog from a deepCoadd:
    instrument = 'LSSTCam-imSim'
    detector = 5
    visit = 924041

    # Run the test
    LVVT1947(instrument, visit, detector)
