# wood_harvest

A python implementation of the CABLE wood harvest product pools.

## Install

Optional: set up a virtualenv

```sh
module load python3
virtualenv my_wood_harvest
source my_wood_harvest/bin/activate
```

Clone and install with pip:

```sh
pip install git+https://gitlab.com/tammasloughran/wood_harvest.git
```

## Usage

```
usage: wood_harvest [-h] [-v WOOD_FLUX_VAR] [-s START_YEAR] [-e END_YEAR] [-w WOOD_HARVEST WOOD_HARVEST WOOD_HARVEST] [-f HARVEST_FRAC HARVEST_FRAC HARVEST_FRAC] [-t TAU TAU TAU] wood_flux_file

Run wood harvest submodel.

positional arguments:
  wood_flux_file        Input netCDF wood flux file

options:
  -h, --help            show this help message and exit
  -v WOOD_FLUX_VAR, --var-name WOOD_FLUX_VAR
                        Variable name of wood flux data
  -s START_YEAR, --start-year START_YEAR
                        Start year of the run
  -e END_YEAR, --end-year END_YEAR
                        End year of the run
  -w WOOD_HARVEST WOOD_HARVEST WOOD_HARVEST, --wood-harvest WOOD_HARVEST WOOD_HARVEST WOOD_HARVEST
                        Initial wood harvest product pool size
  -f HARVEST_FRAC HARVEST_FRAC HARVEST_FRAC, --harvest-frac HARVEST_FRAC HARVEST_FRAC HARVEST_FRAC
                        Fraction of harvest allocated to wood product pools
  -t TAU TAU TAU, --tau TAU TAU TAU
                        Decay rate of wood product pools (year^-1)

```
