#!/usr/bin/env python3
"""Optimization of the Net Biosphere Productivity (NBP) from modified wood harvest paramters.
"""
import numpy as np
import netCDF4 as nc
import scipy

import ipdb
from wood_harvest import decay
from wood_harvest.input_output import open_wood_flux, load_ncyears

START_YEAR = 1850
END_YEAR = 2014
NYEARS = END_YEAR - START_YEAR + 1
NPFTS = 4
NLATS = 145
NLONS = 192
NPOOLS = 3
FRAC_FILE = '/g/data/p66/tfl561/archive_data/HI-05/frac_HI-05_1850-2014.nc'
AREA_FILE = '/g/data/p66/tfl561/archive_data/HI-05/cell_area.nc'
WOOD_FLUX_FILE = '/g/data/p66/tfl561/archive_data/HI-05/wood_flux_HI-05_1850-2014_global_sum.nc'
NBP_HOFFMAN_FILE = 'data/nbp_hoffman_cumsum.npy'
NBP_HOFFMAN = np.load(NBP_HOFFMAN_FILE)
# Open the wood flux file
ncfile = open_wood_flux(WOOD_FLUX_FILE)
# Load the years in the wood_flux file.
ncyears = load_ncyears(ncfile)
# Create list of years to run over.
years = list(range(START_YEAR, END_YEAR+1))
NEP_FILE = 'data/nep_access_cumsum.npy'
nep = np.load(NEP_FILE)


def nbp_residuals(x:np.ndarray)->np.ndarray:
    """Residuals function to be used to minimize the difference between the Hoffman NBP and the
    python harvest model NBP.
    """
    history_wood_harvest_global, history_wood_respiration_global = decay.run_harvest(
            years,
            ncyears,
            ncfile,
            'wood_flux',
            x[0:3],
            [0.33,0.33,0.34],
            [1.0,0.1,0.01],
            )
    # Load wood_harvest data numpy files.
    fractions = np.load('data/fractions.npy')
    cell_area = nc.Dataset(AREA_FILE, 'r').variables['cell_area'][:]
    land_area = nc.Dataset('data/land_area.nc', 'r').variables['areacella'][:]
    wood_respiration = np.ones((NPOOLS,NYEARS,NPFTS,NLATS,NLONS))*np.nan
    wood_harvest = np.ones((NPOOLS,NYEARS,NPFTS,NLATS,NLONS))*np.nan
    for i,year in enumerate(range(START_YEAR, END_YEAR + 1)):
        for j in range(NPOOLS):
            wood_respiration[j,i] = np.load(f'output/wood_respiration_{j+1}_python_{year}.npy')
    wood_respiration = np.sum(wood_respiration, axis=0)
    wood_respiration *= cell_area
    wood_respiration_series = np.nansum(wood_respiration, axis=(-1,-2,-3))/1e15

    nbp_python_cumsum = nep + np.cumsum(wood_respiration_series)
    residuals = nbp_python_cumsum[:-4] - NBP_HOFFMAN
    return np.sqrt(np.sum(residuals**2)/residuals.size)


results = scipy.optimize.minimize(nbp_residuals, np.array([0,10,35]))
ipdb.set_trace()
