#!/bin/bash

cdo selname,ClearProd -seltimestep,150 /g/data/p66/jk8585/cru_out_LUC_1700_1900.nc clearprod_CABLE-POP_1850.nc
cdo selname,HarvProd -seltimestep,150 /g/data/p66/jk8585/cru_out_LUC_1700_1900.nc harvprod_CABLE-POP_1850.nc
cdo add clearprod_CABLE-POP_1850.nc harvprod_CABLE-POP_1850.nc wood_harvest_CABLE-POP_1850.nc
cdo griddes ../../archive_data/HI-05/frac_HI-05_1850-2014.nc > ACCESS.grid
cdo remapcon2,ACCESS.grid wood_harvest_CABLE-POP_1850.nc wood_harvest_regrid_1850.nc
ncks -d nprod,0 wood_harvest_regrid_1850.nc wood_harvest_1_regrid_1850.nc
ncks -d nprod,1 wood_harvest_regrid_1850.nc wood_harvest_2_regrid_1850.nc
ncks -d nprod,2 wood_harvest_regrid_1850.nc wood_harvest_3_regrid_1850.nc
cdo -L sellevidx,1/4 -selmonth,1 -selyear,1850 ../../archive_data/HI-05/frac_HI-05_1850-2014.nc fracs.nc
cdo -L sellevidx,10 -selmonth,1 -selyear,1850 ../../archive_data/HI-05/frac_HI-05_1850-2014.nc temp.nc
cdo -L mul temp.nc fracs.nc zeros.nc
cdo -L addc,1 zeros.nc ones.nc
cdo -L vertsum fracs.nc total.nc
cdo -L div fracs.nc total.nc fracs2.nc
cdo -L mul total.nc ones.nc mask.nc
cdo -L ifthenelse mask.nc fracs2.nc zeros.nc fracs3.nc
cdo mul wood_harvest_1_regrid_1850.nc fracs3.nc wood_harvest_1_regrid2_1850.nc
cdo mul wood_harvest_2_regrid_1850.nc fracs3.nc wood_harvest_2_regrid2_1850.nc
cdo mul wood_harvest_3_regrid_1850.nc fracs3.nc wood_harvest_3_regrid2_1850.nc
