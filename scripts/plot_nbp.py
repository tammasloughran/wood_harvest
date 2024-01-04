#!/usr/bin/env python3
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

START_YEAR = 1850
END_YEAR = 2014
NYEARS = END_YEAR - START_YEAR + 1
NPFTS = 4
NLATS = 145
NLONS = 192
NPOOLS = 3
FRAC_FILE = '/g/data/p66/tfl561/archive_data/HI-05/frac_HI-05_1850-2014.nc'
AREA_FILE = '/g/data/p66/tfl561/archive_data/HI-05/cell_area.nc'

# Use saved numpy arrays?
saved = True

if not saved:
    # Load the Hoffman nbp data
    ncfile = nc.Dataset('data/nbp_hoffman_1850-2010.nc', 'r')
    nbp_hoffman = ncfile.variables['nbp'][:].squeeze()*-1
    ncfile.close()
    nbp_hoffman_cumsum = np.cumsum(nbp_hoffman)
    np.save('data/nbp_hoffman_cumsum.npy', nbp_hoffman_cumsum.data)

    # Load the NBP for ACCESS
    ncfile = nc.Dataset('data/Hoffman_ACCESS-ESM1-5.nc', 'r')
    nbp_access_cumsum = ncfile\
            .groups['MeanState']\
            .variables['accumulate_of_nbp_over_global'][:]\
            .squeeze()
    ncfile.close()
    np.save('data/nbp_access_cumsum.npy', nbp_access_cumsum.data)

    # Load the NEE from ACCESS
    ncfile = nc.Dataset('data/nep_respiration_gobal_sum.nc')
    nep = ncfile.variables['nep'][:].squeeze()*-1
    ncfile.close()
    np.save('data/nep_access_cumsum.npy', nep.data)

    # Load ACCESS wood resp
    ncfile = nc.Dataset('data/wood_respiration_gobal_sum.nc')
    access_wood_resp = ncfile.variables['wood_respiration_1'][:].squeeze()*-1
    ncfile.close()
    np.save('data/wood_resp_access_cumsum.npy', access_wood_resp.data)

    my_nbp = nep - access_wood_resp
    np.save('data/mynbp_access_cumsum.npy', my_nbp.data)
else:
    nbp_hoffman_cumsum = np.load('data/nbp_hoffman_cumsum.npy')
    nbp_access_cumsum = np.load('data/nbp_access_cumsum.npy')
    nep = np.load('data/nep_access_cumsum.npy')
    my_nbp = np.load('data/mynbp_access_cumsum.npy')
    access_wood_resp = np.load('data/wood_resp_access_cumsum.npy')


# Load wood_harvest data numpy files.
fractions = np.load('data/fractions.npy')
cell_area = nc.Dataset(AREA_FILE, 'r').variables['cell_area'][:]
land_area = nc.Dataset('data/land_area.nc', 'r').variables['areacella'][:]
wood_respiration = np.ones((NPOOLS,NYEARS,NPFTS,NLATS,NLONS))*np.nan
wood_harvest = np.ones((NPOOLS,NYEARS,NPFTS,NLATS,NLONS))*np.nan
for i,year in enumerate(range(START_YEAR, END_YEAR + 1)):
    print(year, end='\r')
    for j in range(NPOOLS):
        wood_respiration[j,i] = np.load(f'output/wood_respiration_{j+1}_python_{year}.npy')
wood_respiration = np.sum(wood_respiration, axis=0)
wood_respiration *= cell_area
wood_respiration_series = np.nansum(wood_respiration, axis=(-1,-2,-3))/1e15

nbp_python_cumsum = nep + np.cumsum(wood_respiration_series)

plt.figure()
plt.plot(range(1850, 2011), nbp_hoffman_cumsum, color='gray', label='Hoffman')
plt.plot(range(1850, 2012), nbp_access_cumsum, color='red', label='ACCESS-ESM1-5 NBP')
plt.plot(range(1850, 2015), nep, color='pink', label='ACCESS NEP')
plt.plot(range(1850, 2015), access_wood_resp*-1, color='orange', label='ACCESS wood_resp')
plt.plot(range(1850, 2015), nbp_python_cumsum, color='blue', label='python')
plt.plot(range(1850, 2015), my_nbp, color='green', label='mynbp')
plt.plot(range(1850, 2015), np.cumsum(wood_respiration_series), color='purple', label='python respo')
plt.ylabel('Pg(C)')
plt.xlabel('Time (year)')
plt.hlines(0, 1850, 2015, color='black')
plt.legend()
plt.show()
