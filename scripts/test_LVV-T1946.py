# Test script for LSST Data Management acceptance test campaign
# LVV-T1946:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T1946>
# LVV-T1946 tests verification element LVV-178, <https://jira.lsstcorp.org/browse/LVV-178>
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

def LVVT1946(tract, patch, band):
    """ Execute test case LVV-T1946

    Parameters
    ----------
    tract: `int`
        Input tract for test.
    patch: `int`
        Input patch for test.
    band: `str`
        Band on which to test schema.
    """

    dataIdCoadd = {'tract':tract, 'band':band, 'patch':patch}
    print('Input dataId: ', dataIdCoadd)

    try:
        forced_src = butler.get('deepCoadd_forced_src', dataId = dataIdCoadd)
    except:
        print('Invalid dataId. Please check and try again.')

    fsch = forced_src.schema
    forced_src_flag = check_schema(fsch)

    # If any of the units are not "count," print "FALSE."
    assert(np.all(forced_src_flag)), 'FALSE: not all instFlux entries have units of counts.'
    
    # If all of the flux units are "count," print "TRUE."
    print('\n All forced_src instFlux entries have units of counts: ', np.all(forced_src_flag))


def check_schema(sch):
    """ Check the units on each flux entry in the schema

    Parameters
    ----------
    sch: Schema 
        forced_src schema to check

    Returns
    -------
    forced_src_flag: `list` of `bool`
        Boolean list containing "True" for elements with flux units in "count"
    """

    forced_src_flag = []
    for entry in sch:
        field = entry.getField().getName()
        if 'instFlux' in field and 'flag' not in field and 'Cov' not in field:
            flux_units = entry.getField().getUnits()
            forced_src_flag.append('count' in flux_units)
            print(f'{field:60}..... {flux_units:20}')
    return forced_src_flag


if __name__ == "__main__":

    # Select an arbitrary source catalog from a deepCoadd:
    band = 'i'
    tract = 3828
    patch = 13

    # Run the test
    LVVT1946(tract, patch, band)
