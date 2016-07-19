import numpy as np
from skimage.segmentation import quickshift, mark_boundaries
from skimage import measure
from scipy import misc

#TODO filepath as argument to script
# Image path
filePath = "C:\\Users\\Phil\\Desktop\\Sea Ice Photo for XSEDE16\\Examples\\072610_00022.jpg"

#TODO Classifier filepath as argument to script
# Pre-trained classifier path
forestFilePath = "fittedforest.p"

# Quickshift parameters
qs_kernel_size = 3
qs_max_dist = 6
qs_ratio = 0.5

#TODO should use getImage
img = misc.imread(filePath)

# Quickshift segment image
segments_quick = quickshift(img, kernel_size=qs_kernel_size, max_dist=qs_max_dist, ratio=qs_ratio)
print("Quickshift number of segments: %d" % len(np.unique(segments_quick)))

# Extract feature properties
# Mean RGB intensities
props = measure.regionprops(segments_quick,img[:,:,0], cache=False)
r=[prop.mean_intensity for prop in props]
props = measure.regionprops(segments_quick,img[:,:,1], cache=False)
g=[prop.mean_intensity for prop in props]
props = measure.regionprops(segments_quick,img[:,:,2], cache=False)
b=[prop.mean_intensity for prop in props]
# RGB Ratios
Ratio1 = np.divide(np.subtract(b,r) , np.add(b,r))
Ratio2 = np.divide(np.subtract(b,g) , np.add(b,g))
Ratio3 = np.divide(np.subtract(g,r) , np.subtract(np.subtract(np.multiply(b,2),g),r))
# Stack properties to array
features = np.column_stack((r,g,b,Ratio1,Ratio2,Ratio3))

# Load pretrained classifier
import pickle
forest = pickle.load( open( forestFilePath , "rb" ) )

# Predict
output = forest.predict(features)
