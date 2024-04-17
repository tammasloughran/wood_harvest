#!/bin/bash
# The wrong way to calculate wood respiration. This is the only way I can
# replicate the CMORized ACCESS-ESM1-5 output published on /g/data/fs38.

# Multiply the pft level raw wood_respiration_1/2/3 output by the land frac file
# Land frac file is in % so it needs to be divided by 100 later.
# This is wrong because the wood respiration is output on PFTs and it
# needs to be multiplied by the tile fractions in stead.
cdo -L \
    -mul \
        /g/data/p66/tfl561/archive_data/HI-05/wood_respiration_1_HI-05_1850-2014.nc \
        /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/fx/sftlf/gn/latest/sftlf_fx_ACCESS-ESM1-5_historical_r1i1p1f1_gn.nc \
    wood_respiration_1_by_land_frac.nc

cdo -L \
    -mul \
        /g/data/p66/tfl561/archive_data/HI-05/wood_respiration_2_HI-05_1850-2014.nc \
        /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/fx/sftlf/gn/latest/sftlf_fx_ACCESS-ESM1-5_historical_r1i1p1f1_gn.nc \
    wood_respiration_2_by_land_frac.nc

cdo -L \
    -mul \
        /g/data/p66/tfl561/archive_data/HI-05/wood_respiration_3_HI-05_1850-2014.nc \
        /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/fx/sftlf/gn/latest/sftlf_fx_ACCESS-ESM1-5_historical_r1i1p1f1_gn.nc \
    wood_respiration_3_by_land_frac.nc

# Add up the respirations from each product pool, then add up along pfts, then
# convert from g m-2 year-1 to kg m-2 s-1
cdo -L \
    -divc,1000 \
    -divc,365.25 \
    -divc,24 \
    -divc,60 \
    -divc,60 \
    -divc,100 \
    -vertsum \
    -add -add \
        wood_respiration_1_by_land_frac.nc \
        wood_respiration_2_by_land_frac.nc \
        wood_respiration_3_by_land_frac.nc \
    wood_total.nc

# The correct procedure (Based only on the metadata in the output files) should be:
# - multiply by tile_frac
# - sum all tiles
# - add up respiration for the 3 pools
# - convert units from g m-2 year-1 to kg m-2 s-1
#
# tilesum(sum(wood_i x tile_frac))/100/1000/60/60/24/365.25
# However, the model output for wood respiration does not need to be multiplied by the cover
# fractions. Aparently it has already been done, so it just needs to be multiplied by the land
# fraction.

# Compare the two, they should be almost the same
ncview wood_total.nc & ncview /g/data/fs38/publications/CMIP6/CMIP/CSIRO/ACCESS-ESM1-5/historical/r1i1p1f1/Emon/fProductDecomp/gn/latest/fProductDecomp_Emon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_185001-201412.nc
