# Wood harvest decay module.
import math

import numpy as np

N_WOOD_POOLS = 3


def decay_wood_harvest(harvest_pool:np.ndarray, tau:float)->np.ndarray:
    """Calculate the respiration of the wood harvest pool.

    harvest_pool - initial size of the wood harvest pool
    tau - decay rate of the wood harvest pool in $year^{-1}$
    """
    return harvest_pool*(1.0 - math.exp(-tau))


def run_harvest(
        years,
        ncyears,
        ncfile,
        varname,
        wood_harvest,
        harvest_frac,
        tau,
        ):
    """Run the simulation of wood harvest and decay.

    years - sequence of years to run the simulation over.
    ncyears - sequence of years in the netcdf file.
    ncfile - the open netcdf `wood_flux` file.
    varname - ncfile's `wood_flux` variable name.
    wood_harvest - the initial `wood_harvest` pool.
    harvest_frac - the proprotion of harvested mass allocated to the product pools.
    tau - the decay rate of the wood product pools.
    """
    # Initialize history variables
    history_wood_harvest_global = []
    history_wood_respiration_global = []

    for year in years:
        wood_respiration = [0.0,0.0,0.0]

        # Load the harvested wood flux `wood_flux` data.
        iyear = np.where(ncyears==year)[0][0] # This is annual average, so I only need 1 value.
        wood_flux = ncfile.variables[varname][iyear,1:4,...].squeeze().data
        wood_flux[wood_flux<0] = np.nan

        for n in range(N_WOOD_POOLS):
            # Distribute the harvested wood to the `wood_harvest` pools for each harvest fraction.
            wood_harvest[n] += wood_flux*harvest_frac[n]

            # Calculate the `wood_respiration`.
            wood_respiration[n] = decay_wood_harvest(wood_harvest[n], tau[n])

            # Apply the decay to each `wood_harvest` pool.
            wood_harvest[n] -= wood_respiration[n]

            # Output variables.
            np.save(f'output/wood_harvest_{n+1}_python_{year}.npy', wood_harvest[n])
            np.save(f'output/wood_respiration_{n+1}_python_{year}.npy', wood_respiration[n])

        # Summarise to history variables
        wood_harvest_global = 0
        for n in range(N_WOOD_POOLS):
            wood_harvest_global += np.nansum(wood_harvest[n], axis=(-1,-2,-3))
        history_wood_harvest_global.append(wood_harvest_global)
        wood_respiration_global = 0
        for n in range(N_WOOD_POOLS):
            wood_respiration_global += np.nansum(wood_respiration[n], axis=(-1,-2,-3))
        history_wood_respiration_global.append(wood_respiration_global)
        print(year, wood_harvest_global, wood_respiration_global)

    return history_wood_harvest_global, history_wood_respiration_global
