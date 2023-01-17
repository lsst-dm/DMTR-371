# Test script for LSST Data Management acceptance test campaign
# LVV-T66:<https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T66>
# LVV-T66 tests verification element LVV-99, <https://jira.lsstcorp.org/browse/LVV-99>
# which verifies requirement DMS-REQ-0268-V-01: Forced-Source Catalog
#
# The lsst environment must be set up to run this test,
# see <https://pipelines.lsst.io/install/setup.html> for more details

import os
import numpy as np
from lsst.daf.butler import Butler

# Confirm the version of the Science Pipelines:
os.system('eups list -s | grep lsst_distrib')

# For RC2 data on the USDF:
repo = '/sdf/group/rubin/repo/main'
collection = 'HSC/runs/RC2/w_2022_24/DM-35231'

butler = Butler(repo, collections=collection)

# Query the Butler for all visit/detector combinations overlapping tract 9615:
dids = []

for data_id in butler.registry.queryDataIds(
    ["tract", "visit", "detector"],
    instrument="HSC",
    skymap='hsc_rings_v1',
    datasets="visitSummary",
    collections=collection,
    where="tract=9615 AND patch=43",
    ):

    dids.append(data_id)

# Extract the ObjectTable for tract 9615
cols = 'objectId'
objs = butler.get('objectTable_tract', tract=9615, skymap='hsc_rings_v1',
                  parameters={'columns':cols})

# For each dataId returned by the query above, check that:
# (1) PSF and aperture fluxes, and their errors, have been measured
# (2) All objectIds have associated forced-source measurements

psf_flux_flag = []
psf_flux_err_flag = []
ap_flux_flag = []
ap_flux_err_flag = []
frac_obj = []
i = 0

for did in dids:
    try:
        # Get the forced source table for the particular visit/detector
        fs = butler.get('forced_src', dataId=did)
        fs_df = fs.asAstropy().to_pandas()

        # Extract flux measurements
        psfflux = fs['base_PsfFlux_instFlux']
        psfflux_err = fs['base_PsfFlux_instFluxErr']
        apflux = fs['base_CircularApertureFlux_9_0_instFlux']
        apflux_err = fs['base_CircularApertureFlux_9_0_instFluxErr']

        # Create boolean flags that are True if all fluxes and errors are populated
        #   with real numbers, and False otherwise:
        psf_flux_flag.append(np.all(np.isreal(psfflux)))
        psf_flux_err_flag.append(np.all(np.isreal(psfflux_err)))
        ap_flux_flag.append(np.all(np.isreal(apflux)))
        ap_flux_err_flag.append(np.all(np.isreal(apflux_err)))
    
        # Calculate the fraction of forced sources that are in the ObjectTable
        #   (based on objectIds):
        frac_in_obj = np.sum(fs_df['objectId'].isin(objs.index.values))/len(fs_df)
        frac_obj.append(frac_in_obj)

        # print(frac_in_obj)
        if frac_in_obj < 1.0:
            print('Less than one. DataId: ', did)
    except:
        pass

    i += 1
    if np.mod(i, 100) < 1:
        print(i, ' of ', len(dids))


print('\nResults for ', len(psf_flux_flag), 'visit/detectors that overlap the input tract.\n')

print('psfflux check: ', np.alltrue(np.array(psf_flux_flag)))
print('psfflux_err check: ', np.alltrue(np.array(psf_flux_err_flag)))
print('apflux check: ', np.alltrue(np.array(ap_flux_flag)))
print('apflux_err check: ', np.alltrue(np.array(ap_flux_err_flag)))

print('All objects have forced sources? ', np.all(np.array(frac_obj) > 0.999))

del objs
del fs

# Extract the forcedSourceOnDiaObjectTable for tract 9615
cols = 'diaObjectId'
dia_objs = butler.get('forcedSourceOnDiaObjectTable_tract', tract=9615, skymap='hsc_rings_v1',
                      parameters={'columns':cols})

# For each dataId returned by the query above, check that:
# (1) PSF and aperture fluxes, and their errors, have been measured
# (2) All objectIds have associated forced-source measurements

dia_psf_flux_flag = []
dia_psf_flux_err_flag = []
dia_frac_obj = []
i = 0

for did in dids:
    # Get the forced source table for the particular visit/detector
    try:
        dfs = butler.get('forced_src_diaObject', dataId=did)
        dfs_df = dfs.asAstropy().to_pandas()

        # Extract flux measurements
        dia_psfflux = dfs['base_PsfFlux_instFlux']
        dia_psfflux_err = dfs['base_PsfFlux_instFluxErr']

        # Create boolean flags that are True if all fluxes and errors are populated
        #   with real numbers, and False otherwise:
        dia_psf_flux_flag.append(np.all(np.isreal(dia_psfflux)))
        dia_psf_flux_err_flag.append(np.all(np.isreal(dia_psfflux_err)))
    
        # Calculate the fraction of forced sources that are in the ObjectTable
        #   (based on objectIds):
        dia_frac_in_obj = np.sum(dfs_df['diaObjectId'].isin(dia_objs['diaObjectId']))/len(dfs_df)
        dia_frac_obj.append(dia_frac_in_obj)

        # print(dia_frac_in_obj)
        if dia_frac_in_obj < 1.0:
            print('Less than one. DataId: ', did)
    except:
        # print('No forced_src_diaObject found for ', did)
        pass

    i += 1
    if np.mod(i, 100) < 1:
        print(i, ' of ', len(dids))


print('\nResults for ', len(dia_psf_flux_flag), 'visit/detectors that overlap the input tract.\n')

print('DIA psfflux check: ', np.alltrue(np.array(dia_psf_flux_flag)))
print('DIA psfflux_err check: ', np.alltrue(np.array(dia_psf_flux_err_flag)))

print('DIA: All objects have forced sources? ', np.all(np.array(dia_frac_obj) > 0.999))

dia_diff_psf_flux_flag = []
dia_diff_psf_flux_err_flag = []
dia_diff_frac_obj = []
i = 0

for did in dids:
    # Get the forced source table for the particular visit/detector
    try:
        dfsdiff = butler.get('forced_diff_diaObject', dataId=did)
        dfsdiff_df = dfsdiff.asAstropy().to_pandas()

        # Extract flux measurements
        dia_diff_psfflux = dfsdiff['base_PsfFlux_instFlux']
        dia_diff_psfflux_err = dfsdiff['base_PsfFlux_instFluxErr']

        # Create boolean flags that are True if all fluxes and errors are populated
        #   with real numbers, and False otherwise:
        dia_diff_psf_flux_flag.append(np.all(np.isreal(dia_diff_psfflux)))
        dia_diff_psf_flux_err_flag.append(np.all(np.isreal(dia_diff_psfflux_err)))
    
        # Calculate the fraction of forced sources that are in the ObjectTable
        #   (based on objectIds):
        dia_diff_frac_in_obj = np.sum(dfsdiff_df['diaObjectId'].isin(dia_objs['diaObjectId']))/len(dfsdiff_df)
        dia_diff_frac_obj.append(dia_diff_frac_in_obj)

        # print(dia_frac_in_obj)
        if dia_diff_frac_in_obj < 1.0:
            print('Less than one. DataId: ', did)
    except:
        # print('No forced_src_diaObject found for ', did)
        pass

    i += 1
    if np.mod(i, 100) < 1:
        print(i, ' of ', len(dids))


print('\nResults for ', len(dia_diff_psf_flux_flag), 'visit/detectors that overlap the input tract.\n')

print('DIA diffim psfflux check: ', np.alltrue(np.array(dia_diff_psf_flux_flag)))
print('DIA diffim psfflux_err check: ', np.alltrue(np.array(dia_diff_psf_flux_err_flag)))

print('DIA diffim: All objects have forced sources? ', np.all(np.array(dia_diff_frac_obj) > 0.999))

