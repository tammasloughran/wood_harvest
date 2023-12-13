#!/usr/bin/env python3
# Main program to run the wood harvest submodel.
import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from wood_harvest.decay import decay_wood_harvest, run_harvest
from wood_harvest.input_output import load_access, load_access_global, \
        open_wood_flux, load_ncyears, load_harvest_pool
from wood_harvest.plotting import plot_wood

def main():
    # Parse arguments.
    parser = argparse.ArgumentParser(description="Run wood harvest submodel.")
    parser.add_argument('-v', '--var-name',
            dest='wood_flux_var',
            type=str,
            required=False,
            default='wood_flux',
            help="Variable name of wood flux data",
            )
    parser.add_argument('wood_flux_file',
            type=str,
            help="Input netCDF wood flux file",
            )
    parser.add_argument('-s', '--start-year',
            dest='start_year',
            type=int,
            required=False,
            default=1850,
            help="Start year of the run",
            )
    parser.add_argument('-e', '--end-year',
            dest='end_year',
            type=int,
            required=False,
            default=2014,
            help="End year of the run",
            )
    parser.add_argument('-w', '--wood-harvest',
            dest='wood_harvest',
            nargs=3,
            required=False,
            default=['0.0','0.0','0.0'],
            help="Initial wood harvest product pool size",
            )
    parser.add_argument('-f', '--harvest-frac',
            dest='harvest_frac',
            nargs=3,
            type=float,
            required=False,
            default=[0.33,0.33,0.34],
            help="Fraction of harvest allocated to wood product pools",
            )
    parser.add_argument('-t', '--tau',
            dest='tau',
            nargs=3,
            type=float,
            required=False,
            default=[1.0,0.1,0.01],
            help="Decay rate of wood product pools (year^-1)",
            )
    args = parser.parse_args()


    # Open the wood flux file
    ncfile = open_wood_flux(args.wood_flux_file)

    # Load the years in the wood_flux file.
    ncyears = load_ncyears(ncfile)

    # Create list of years to run over.
    years = list(range(args.start_year, args.end_year+1))

    # Load initial wood harvest pools
    for i in range(len(args.wood_harvest)):
        if args.wood_harvest[i][-3:]=='.nc':
            args.wood_harvest[i] = load_harvest_pool(args.wood_harvest[i])
        else:
            args.wood_harvest[i] = float(args.wood_harvest[i])

    # Run the simulation
    if not os.path.isdir('./output'):
        os.mkdir('output')
    print("year wood_harvest wood_respiration")
    history_wood_harvest_global, history_wood_respiration_global = run_harvest(
            years,
            ncyears,
            ncfile,
            args.wood_flux_var,
            args.wood_harvest,
            args.harvest_frac,
            args.tau,
            )

    # Close the wood flux file.
    ncfile.close()

    # Load the ACCESS results.
    if history_wood_harvest_global[-1]<100:
        access_wood_harvest, access_wood_respiration = load_access_global()
    else:
        access_wood_harvest, access_wood_respiration = load_access()

    # Plot the results
    plot_wood(
            years,
            history_wood_harvest_global,
            access_wood_harvest,
            'g(C)/m2',
            'Global sum of wood harvest product pools',
            )
    plot_wood(
            years,
            history_wood_respiration_global,
            access_wood_respiration,
            'g(C)/m2/year',
            'Global sum of wood products respiration',
            )
    plt.show()

