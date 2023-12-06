# Input output routines
import os

import netCDF4 as nc
import numpy as np

from wood_harvest.tools import yearly_mean_from_monthly


def load_access_file(infile:str, var:str)->np.ndarray:
    """Load global and PFT sum of an ACCESS wood data file. Loads only the woody PFTs.
    infile - input filename
    var - name of variable to load
    """
    accessnc = nc.Dataset(infile, 'r')
    access_data = accessnc.variables[var][:,0:4,...].sum(axis=(-1,-2,-3))
    accessnc.close()
    return access_data


def load_access():
    """Load the ACCESS wood_harvest and wood_respiration.
    """
    if not os.path.isfile('access_wood_harvest.npy'):
        access_wood_harvest = load_access_file(
                '/g/data/p66/tfl561/archive_data/HI-05/wood_harvest_1_HI-05_1850-2014.nc',
                'wood_harvest_1',
                )
        access_wood_harvest += load_access_file(
                '/g/data/p66/tfl561/archive_data/HI-05/wood_harvest_2_HI-05_1850-2014.nc',
                'wood_harvest_2',
                )
        access_wood_harvest += load_access_file(
                '/g/data/p66/tfl561/archive_data/HI-05/wood_harvest_3_HI-05_1850-2014.nc',
                'wood_harvest_3',
                )
        access_wood_harvest = yearly_mean_from_monthly(access_wood_harvest)
        np.save('access_wood_harvest.npy', access_wood_harvest.data)

        access_wood_respiration = load_access_file(
                '/g/data/p66/tfl561/archive_data/HI-05/wood_respiration_1_HI-05_1850-2014.nc',
                'wood_respiration_1',
                )
        access_wood_respiration += load_access_file(
                '/g/data/p66/tfl561/archive_data/HI-05/wood_respiration_2_HI-05_1850-2014.nc',
                'wood_respiration_2',
                )
        access_wood_respiration += load_access_file(
                '/g/data/p66/tfl561/archive_data/HI-05/wood_respiration_3_HI-05_1850-2014.nc',
                'wood_respiration_3',
                )
        access_wood_respiration = yearly_mean_from_monthly(access_wood_respiration)
        np.save('access_wood_respiration.npy', access_wood_respiration.data)
    else:
        access_wood_harvest = np.load('access_wood_harvest.npy')
        access_wood_respiration = np.load('access_wood_respiration.npy')

    return access_wood_harvest, access_wood_respiration


def open_wood_flux(wood_flux_file):
    """Open the wood_flux file for reading.
    """
    return nc.Dataset(wood_flux_file, 'r')


def load_ncyears(ncfile):
    """Load the monthly array of the years in the wood flux file.
    """
    times = ncfile.variables['time'][:]
    dates = nc.num2date(times, ncfile.variables['time'].units)
    return np.array([d.year for d in dates])


def load_harvest_pool(infile:str):
    """Load an initial wood harvest pool.

    infile - input file name
    """
    ncfile = nc.Dataset(infile, 'r')
    for var in list(ncfile.variables.keys()):
        if ncfile.variables[var].ndim>2:
            selvar = var
    data = ncfile.variables[selvar][-1,0:4,...].squeeze().data
    data[data>1e5] = np.nan
    data[data<-1e5] = np.nan
    data[data<0] = 0
    return data

