# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
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

properties = measure.regionprops(segments_quick, img[:,:,1])
[prop.area for prop in properties]

[prop.mean_intensity for prop in properties]
#for prop in region:
#    print(prop, region[prop])





