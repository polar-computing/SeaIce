# SeaIce
Quantifying aerosol presence and composition over Earth's ice sheets and glaciers - mapping anthropogenic and natural aerosol patters and estimating changes over time

# Decription
Many of Earth’s glaciers have been losing mass at an alarming rate in the past few decades. Both anthropogenic and natural aerosols deposited on snow and ice can darken reflective surfaces, increase solar absorption and subsequently enhance snow and ice melt rates. This project seeks to map aerosols over Earth's land ice using the global land ice identification mask and monthly mean MERRA-2 aerosol data. Ideally, the project will be completed for all of Earth, mapping aerosol concentrations, with seasonal and annual totals from 1980-present. If time/space limits us, the project can be reduced geographically (e.g. Arctic or Himalaya) and temporally (2000-present).

# Code
If time allows, desire to add land ice surface reflectance values from Landsat (all mountain, peninsula, coastal glaciers) and MODIS for Antarctic and Greenland ice sheets. Reflectance data will be collected to coincide with measured aerosol season or year (e.g. spring or annual).
Landsat, raster, surface reflectance data
To learn more and access data see:
http://landsat.usgs.gov/CDR_LSR.php
File size ~2.5 GB per Landsat scene, all 7 spectral bands, 190 km x 180 km area per file.

MODIS, raster, 8-day surface reflectance data, to be collected coinciding with season or year corresponding to aerosol data.
To learn more and access data see:
https://lpdaac.usgs.gov/dataset_discovery/modis/modis_products_table/myd09a1
File size ~80 MB per tile, all 7 spectral bands, one tile. 460 tiles to cover Earth, tiles are 10 degrees by 10 degrees at the equator (http://modis-land.gsfc.nasa.gov/MODLAND_grid.html).


# Data
## Input data:
[Randolph Glacier Inventory](http://www.glims.org/RGI/rgi50_dl.html), RGI 5.0, shapefile, vector format, delineates the spatial extent of Earth’s glaciers.

file size: whole inventory 410 mb zipped
739 MB unzipped, 125 files, organized by 19 regions

MERRA-2 aerosol raster [data](http://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/data_access/). Will look at monthly mean dust, organic carbon, black carbon, sea salt and sulfate aerosol concentrations.
To get the data, follow directions on this page:
NetCDF-4 file
File sizes ~155 MB per monthly mean file.
More info can be found in this [pdf](http://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf)

# Tools
Potential tools/languages to be used: Python, QGIS, matlab, idl, ArcGIS
