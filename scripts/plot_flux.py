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

single_point = False

if single_point:
    NLATS = 1
    NLONS = 1

# Load fractions.
#ncfrac = nc.Dataset(FRAC_FILE, 'r')
#fractions = ncfrac.variables['frac'][:,:NPFTS].squeeze()
#fractions = fractions[0:-1:12]
#np.save('data/fractions.npy', fractions.data)
fractions = np.load('data/fractions.npy')

# Load the cell area
cell_area = nc.Dataset(AREA_FILE, 'r').variables['cell_area'][:]

# Load the woody_area for single point runs
pft_area = nc.Dataset(
        '/g/data/p66/tfl561/archive_data/HI-05/pft_area_HI-05_1850-2014_global_sum.nc',
        'r',
        ).variables['pft_area'][::12,:4]

# Load wood_harvest data numpy files.
wood_respiration = np.ones((NPOOLS,NYEARS,NPFTS,NLATS,NLONS))*np.nan
wood_harvest = np.ones((NPOOLS,NYEARS,NPFTS,NLATS,NLONS))*np.nan
for i,year in enumerate(range(START_YEAR, END_YEAR + 1)):
    print(year, end='\r')
    for j in range(NPOOLS):
        wood_respiration[j,i] = np.load(f'output/wood_respiration_{j+1}_python_{year}.npy')
        wood_harvest[j,i] = np.load(f'output/wood_harvest_{j+1}_python_{year}.npy')

# Load the ACCESS time series
access_wood_harvest = nc.Dataset(
        '/g/data/p66/tfl561/archive_data/HI-05/wood_harvest_1850-2014_global_sum.nc',
        'r',
        ).variables['wood_harvest_1'][::12].squeeze()
access_wood_respiration = nc.Dataset(
        '/g/data/p66/tfl561/archive_data/HI-05/wood_respiration_1850-2014_global_sum.nc',
        'r',
        ).variables['wood_respiration_1'][::12].squeeze()

# Apply fractions and global sum.
if single_point:
    wood_respiration *= pft_area/1e4*2
    wood_harvest *= pft_area/1e4*2
else:
    wood_respiration *= fractions*cell_area
    wood_harvest *= fractions*cell_area
wood_respiration_series = np.nansum(wood_respiration, axis=(-1,-2,-3))
wood_harvest_series = np.nansum(wood_harvest, axis=(-1,-2,-3))

# Plot the result.
years = np.arange(START_YEAR, END_YEAR + 1)
plt.figure()
plt.plot(years, wood_respiration_series.sum(axis=0)/1e15, label='total')
for i in range(NPOOLS):
    plt.plot(years, wood_respiration_series[i]/1e15, label=f'from pool {i+1}')
plt.plot(years, access_wood_respiration, label='ACCESS')
plt.ylabel('Pg(C)/year')
plt.xlabel('Time (year)')
plt.legend()
plt.title('Wood product respiration')

plt.figure()
plt.plot(years, wood_harvest_series.sum(axis=0)/1e15, label='total')
for i in range(NPOOLS):
    plt.plot(years, wood_harvest_series[i]/1e15, label=f'pool {i+1}')
plt.plot(years, access_wood_harvest, label='ACCESS')
plt.ylabel('Pg(C)')
plt.xlabel('Time (year)')
plt.legend()
plt.title('Wood product pools')

# Load the NEE for ACCESS.
ncfile = nc.Dataset('data/nee_ACCESS-ESM1-5_global_sum.nc', 'r')
nee_access = ncfile.variables['nep'][:].squeeze()*-1
ncfile.close()

# Load the NBP for ACCESS
ncfile = nc.Dataset('data/Hoffman_ACCESS-ESM1-5.nc', 'r')
nbp_access_cumsum = ncfile\
        .groups['MeanState']\
        .variables['accumulate_of_nbp_over_global'][:]\
        .squeeze()
ncfile.close()

# Load the Hoffman nbp data
ncfile = nc.Dataset('data/nbp_hoffman_1850-2010.nc', 'r')
nbp_hoffman = ncfile.variables['nbp'][:].squeeze()*-1
ncfile.close()
nbp_hoffman_cumsum = np.cumsum(nbp_hoffman)

# Add the wood_respiration_series to the nee_access
nbp_python = nee_access + wood_respiration_series.sum(axis=0)/1e15
nbp_python_cumsum = np.cumsum(nbp_python)

plt.figure()
#import ipdb
#ipdb.set_trace()
plt.plot(range(1850, 2011), nbp_hoffman_cumsum, color='gray', label='Hoffman')
plt.plot(range(1850, 2012), nbp_access_cumsum, color='red', label='ACCESS-ESM1-5')
plt.plot(range(1850, 2015), nbp_python_cumsum, color='blue', label='python')
plt.plot(range(1850, 2015), np.cumsum(nee_access), color='orange', label='NEE_access')
plt.ylabel('Pg(C)')
plt.xlabel('Time (year)')
plt.hlines(0, range(1850, 2015))
plt.legend()

plt.show()
