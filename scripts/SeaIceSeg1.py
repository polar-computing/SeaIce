# -*- coding: utf-8 -*-
"""
Sea ice high-spatial-resoluton image segmentation and feature extraction
Author: Xin Miao
Date: 7/18/2016
"""
from __future__ import print_function
from skimage import data
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage import measure

# from skimage.data import astronaut
from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

from sklearn.ensemble import RandomForestClassifier

img = img_as_float(data.load('D:/Sea_Ice_Photo/072610/Examples/072610_00022.jpg'))
#[::2, ::2])
#img = img_as_float(astronaut()[::2, ::2])

#[::2, ::2]
#segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
#segments_slic = slic(img, n_segments=1000, compactness=2, sigma=1)
segments_quick = quickshift(img, kernel_size=3, max_dist=6, ratio=0.5)

#print("Felzenszwalb's number of segments: %d" % len(np.unique(segments_fz)))
#print("Slic number of segments: %d" % len(np.unique(segments_slic)))
print("Quickshift number of segments: %d" % len(np.unique(segments_quick)))

#fig, ax = plt.subplots(1, 3, sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
#fig.set_size_inches(8, 3, forward=True)
#fig.subplots_adjust(0.05, 0.05, 0.95, 0.95, 0.05, 0.05)
#
#ax[0].imshow(mark_boundaries(img, segments_fz))
#ax[0].set_title("Felzenszwalbs's method")
#ax[1].imshow(mark_boundaries(img, segments_slic))
#ax[1].set_title("SLIC")
#ax[2].imshow(mark_boundaries(img, segments_quick))
#ax[2].set_title("Quickshift")
#for a in ax:
#    a.set_xticks(())
#    a.set_yticks(())
#plt.show()

#plt.imshow(mark_boundaries(img,segments_slic))
#plt.imsave('result.jpg', mark_boundaries(img,segments_slic))

plt.imshow(mark_boundaries(img,segments_quick))
plt.imsave('result.jpg', mark_boundaries(img,segments_quick))

#propertiesR = measure.regionprops(segments_quick, img[:,:,0])
#propertiesG = measure.regionprops(segments_quick, img[:,:,1])
#propertiesB = measure.regionprops(segments_quick, img[:,:,2])
##[prop.area for prop in properties]
##properties = measure.regionprops(segments_quick, img)
#RGB=[[prop.mean_intensity for prop in propertiesR], \
#    [prop.mean_intensity for prop in propertiesG], \
#    [prop.mean_intensity for prop in propertiesB]]
#
#Ratio1=[]
#Ratio2=[]
#Ratio3=[]
#
#for i in range (0, len(RGB[0])):
#    Ratio1.append((RGB[2][i]-RGB[0])/(RGB[2][i]+RGB[0][i]))
#    Ratio2.append((RGB[2][i]-RGB[1])/(RGB[2][i]+RGB[1][i]))
#    Ratio3.append((RGB[1][i]-RGB[0])/(2*RGB[2][i]-RGB[0][i]-RGB[1][i]))

props = measure.regionprops(segments_quick,img[:,:,0], cache=False)
r=[prop.mean_intensity for prop in props]
props = measure.regionprops(segments_quick,img[:,:,1], cache=False)
g=[prop.mean_intensity for prop in props]
props = measure.regionprops(segments_quick,img[:,:,2], cache=False)
b=[prop.mean_intensity for prop in props]
Ratio1 = np.divide(np.subtract(b,r),np.add(b,r))
Ratio2 = np.divide(np.subtract(b,g),np.add(b,g))
Ratio3 = np.divide(np.subtract(g,r),np.subtract(np.subtract(np.multiply(b,2),g),r))
features = np.column_stack((r,g,b,Ratio1,Ratio2,Ratio3))

np.savetxt('features.txt', features, delimiter=',')   # X is an array

