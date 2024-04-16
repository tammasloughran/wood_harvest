#!/bin/bash

WOOD_FLUX_GLOBAL=/g/data/p66/tfl561/archive_data/HI-05/wood_flux_HI-05_1850-2014_global_sum_alone.nc
WOOD_FLUX_SPATIAL=/g/data/p66/tfl561/archive_data/HI-05/wood_flux_HI-05_1850-2014.nc

# Wood harvest initial pools.

# Using CABLE-POP 1850 initial pools in global mode
echo "CABLE-POP 1850"
wood_harvest \
    --wood-harvest 13662.98 74828.75 133283.1 \
    $WOOD_FLUX_GLOBAL
mv output wood_harvest_CABLE-POP_global_output

# Using ACCESS-ESM 2014 initial pools in spatial mode
wood_harvest \
    --wood-harvest \
        ../archive_data/HI-HI-05/wood_harvest_1_HI-05_1850-2014.nc \
        ../archive_data/HI-HI-05/wood_harvest_2_HI-05_1850-2014.nc \
        ../archive_data/HI-HI-05/wood_harvest_2_HI-05_1850-2014.nc \
    $WOOD_FLUX_SPATIAL
echo "ACCESS 2014"
python scripts/plot_flux.py
mv output wood_harvest_ACCESS_spatial_output

# Harvest fraction of product pools

# All pool1 
wood_harvest \
    --harvest-frac 1.0 0.0 0.0 \
    $WOOD_FLUX_SPATIAL
echo "All pool1"
python scripts/plot_flux.py
mv output harvest_frac_1_spatial_output

# All pool2
wood_harvest \
    --harvest-frac 0.0 1.0 0.0 \
    $WOOD_FLUX_SPATIAL
echo "All pool2"
python scripts/plot_flux.py
mv output harvest_frac_2_spatial_output

# All pool3
wood_harvest \
    --harvest-frac 0.0 0.0 1.0 \
    $WOOD_FLUX_SPATIAL
echo "All pool3"
python scripts/plot_flux.py
mv output harvest_frac_3_spatial_output

# Turnover

# *5
wood_harvest \
    --tau 5.0 0.1 0.01 \
    $WOOD_FLUX_SPATIAL
echo "Tau fast *5"
python scripts/plot_flux.py
mv output tau_fast5_spatial_output

# *10
wood_harvest \
    --tau 10.0 1.0 0.1 \
    $WOOD_FLUX_SPATIAL
echo "Tau 10.0 1.0 0.1"
python scripts/plot_flux.py
mv output tau_fast_spatial_output

# /10
wood_harvest \
    --tau 0.1 0.01 0.001 \
    $WOOD_FLUX_SPATIAL
echo "Tau 0.1 0.01 0.001"
python scripts/plot_flux.py
mv output tau_slow_spatial_output


