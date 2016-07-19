############################################################## 
# Date: 20/05/16
# Name: plot_atm_dms.py
# Author: Alek Petty
# Description: Script to plot ATM overlaid on a DMS image
# Input requirements: DMS image and ATM data for specific case studies

import matplotlib
matplotlib.use("AGG")
import numpy as np
from pylab import *
import numpy.ma as ma
from glob import glob
from osgeo import osr, gdal
#may need this if reading in ATM data after 2013 (hdf5 format)
#import h5py

imfile='P1'
rawdatapath = '../../../DATA/'
imagePath = rawdatapath+'IMAGERY/'+imfile+'/'
figpath='./Figures/'


image_path = glob(imagePath+imfile+'.tif')

geo = gdal.Open(image_path[0]) 
band1 = geo.GetRasterBand(1)
band2 = geo.GetRasterBand(2)
band3 = geo.GetRasterBand(3)
red = band1.ReadAsArray()
green = band2.ReadAsArray()
blue = band3.ReadAsArray()

QBIRD = (0.299*red + 0.587*green + 0.114*blue)
QBIRD = ma.masked_where(QBIRD<1, QBIRD)


fig = figure(figsize=(5, 5))
ax=gca()
im2 = imshow(QBIRD, vmin = 0, vmax = 255, cmap = cm.gist_gray, rasterized=True)
subplots_adjust(bottom=0.09, left=0.11, top = 0.94, right=0.99, hspace=0.22)
savefig(figpath+imfile+'.png', dpi=300)
close(fig)


