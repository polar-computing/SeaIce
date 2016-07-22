from sklearn.ensemble import RandomForestClassifier
from skimage.segmentation import quickshift
from scipy import misc
from segmentUtils import *
import pickle
import argparse


parser = argparse.ArgumentParser(description="Quicksift + random forest image classification")
parser.add_argument("-i", "--image", help="Image path")
args = parser.parse_args()


# Quickshift parameters
qs_kernel_size = 3
qs_max_dist = 6
qs_ratio = 0.5

# Training Samples parameters
TSn = 20

# Random forest parameters
RF_n_estimators = 100

# Load image
#TODO should use getImage
img = misc.imread(filePath)
print "Image loaded. ", img.shape[0], " x ", img.shape[1]
fig, ax = plt.subplots()
ax.imshow(img)
plt.show(block=True)
print "Segmenting Image"
# Quickshift segment image
segments = quickshift(img, kernel_size=qs_kernel_size, max_dist=qs_max_dist, ratio=qs_ratio)
print("Quickshift number of segments: %d" % len(np.unique(segments)))

# Extract feature properties
# Mean RGB intensities
features = extractSegmentProperties(segments,img)

labels = trainingSamplesMouse(img,segments)
print labels
trainingSet, trainingSetClasses = createTrainingSet(labels,features)

# Create classifier
forest = RandomForestClassifier(n_estimators = RF_n_estimators)

# Fit classifier
forest = forest.fit(trainingSet,trainingSetClasses)

# Predict
output = forest.predict(features)

# Save forest classifier for future use
pickle.dump(forest, open("fittedforest.p", "wb"))

#validate classifier
result_array = reclassify(segments, output)

plt.imshow(result_array)
plt.show()
plt.pause(0.001)
