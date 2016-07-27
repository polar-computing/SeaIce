from segmentUtils import *
import matplotlib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from skimage.segmentation import quickshift
from scipy import misc
import argparse
import os
import sys
import pickle

parser = argparse.ArgumentParser(description="Quicksift + random forest image classification")
parser.add_argument("-i", "--image", help="Image path")
args = parser.parse_args()
print args.image


# Check that the files exist.
if not os.path.isfile(args.image):
	print 'Source file', args.image, 'does not exist.'
	sys.exit()

# Training image path

filePath = args.image

# Quickshift parameters
qs_kernel_size = 3
qs_max_dist = 6
qs_ratio = 0.5

# Training Samples parameters
TSn = 20

# Random forest parameters
RF_n_estimators = 100
filePath = "C:\Projects\SeaIce\match3.JPG"
# Load image
#TODO should use getImage
img = misc.imread(filePath)
print "Image loaded. ", img.shape[0], " x ", img.shape[1]

# Quickshift segment image
print "Segmenting image"
segments = quickshift(img, kernel_size=qs_kernel_size, max_dist=qs_max_dist, ratio=qs_ratio)
print("Quickshift number of segments: %d" % len(np.unique(segments)))

# Extract labels
print "extracting features"
features = extractSegmentProperties(segments,img)

# Create labels
print "Creating training samples"
#TODO Bug in trainingSamples, first call does not update plot, workaround by calling plt.imshow first
plt.imshow(img)
labels = trainingSamplesRand(img,segments,features,50)


# Create training set
trainingSet,trainingSetClasses = createTrainingSet(labels,features)

# Create classifier
forest = RandomForestClassifier(n_estimators = RF_n_estimators)

# Fit classifier
print "Fitting random forest"
forest = forest.fit(trainingSet,trainingSetClasses)

# Predict
output = forest.predict(features)

# Save forest classifier for future use
print "Saving classifier"
pickle.dump(forest, open("fittedforest.p", "wb"))

# Validate classifier
result_array = reclassify(segments,output)

plt.imshow(result_array)
plt.show()
plt.pause(0.001)