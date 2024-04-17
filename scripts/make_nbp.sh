#!/bin/bash
# Script to reproduce the net biome productivity ACCESS simulations with wood thinning.

cdo -L \
    -divc,1e12 \
    -fldsum \
    -timcumsum \
    -yearsum \
    -muldpm \
    -mulc,24 \
    -mulc,60 \
    -mulc,60 \
    -mul npp_HI-EDC-wood_0500-0600.nc land_area.nc npp_cumsum.nc
    
cdo -L \
    -divc,1e12 \
    -fldsum \
    -timcumsum \
    -yearsum \
    -muldpm \
    -mulc,24 \
    -mulc,60 \
    -mulc,60 \
    -mul rh_HI-EDC-wood_0500-0600.nc land_area.nc rh_cumsum.nc
    
cdo -L -add rh_cumsum.nc -mulc,-1 npp_cumsum.nc nep_cumsum.nc

cdo -L -vertsum -mul -mul wood_respiration_1_HI-EDC-wood_0500-0600.nc frac_HI-EDC-wood_0500-0600.nc cell_area.nc wood_respiration_1.nc
cdo -L -vertsum -mul -mul wood_respiration_2_HI-EDC-wood_0500-0600.nc frac_HI-EDC-wood_0500-0600.nc cell_area.nc wood_respiration_2.nc
cdo -L -vertsum -mul -mul wood_respiration_3_HI-EDC-wood_0500-0600.nc frac_HI-EDC-wood_0500-0600.nc cell_area.nc wood_respiration_3.nc
cdo -L -divc,1e15 -timcumsum -yearmonmean -fldsum -add -add wood_respiration_1.nc wood_respiration_2.nc wood_respiration_3.nc wood_respiration.nc

cdo -L -add nep_cumsum.nc wood_respiration.nc nbp_cumsum.nc

