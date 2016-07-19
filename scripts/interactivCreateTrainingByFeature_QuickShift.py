import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import quickshift, mark_boundaries
from skimage import measure
from sklearn.ensemble import RandomForestClassifier
from scipy import misc

# Training image path
filePath = "C:\\Users\\Phil\\Desktop\\Sea Ice Photo for XSEDE16\\Examples\\072610_00022.jpg"

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
denom = np.subtract(np.subtract(np.multiply(b,2),g),r)
denom[denom==0] = 0.05
Ratio3 = np.divide(np.subtract(g,r) , denom)
# Stack properties to array
features = np.column_stack((r,g,b,Ratio1,Ratio2,Ratio3))


# Interactive polygon labels
def trainingSamples(n,preLabels = None):
	labels = []
	plt.imshow(img)
	plt.draw()
	for i in xrange(n):
		# plt.ion()
		index = np.random.randint(1, features.shape[0])
		if index in segments_quick:
			mask = np.zeros(img.shape[:2], dtype = "uint8")
			mask[segments_quick == index] = 2
			bounded = mark_boundaries(img,mask,color=(1,1,0),mode='thick')
			plt.imshow(bounded)
			plt.draw()
			labeled = False
			while not labeled:
				iclass = raw_input("Enter a class (q to quit, s to skip:")
				if iclass == "q":
					return labels
				if iclass == "s":
					labeled = True
					continue
				try:
					iclass = int(iclass)
					labels.append((index,iclass))
					labeled = True
			#append here
				except:
					print "Class must be an integer"
		else:
			print "Feature index out of range"
		if preLabels:
			labels = labels + preLabels
	return labels

# Create labels
#TODO Bug in trainingSamples, first call does not update plot, workaround by calling plt.imshow first
plt.imshow(img)
labels = trainingSamples(50)

# Extract labels and indexes
trainingSetIndex = [x[0]-1 for x in labels]
trainingSetClasses = [x[1] for x in labels]

#create training set
trainingSet = features[trainingSetIndex]

# Create classifier
forest = RandomForestClassifier(n_estimators = RF_n_estimators)

# Fit classifier
forest = forest.fit(trainingSet,trainingSetClasses)

# Predict
output = forest.predict(features)

# Save forest classifier for future use
import pickle
pickle.dump( forest, open( "fittedforest.p", "wb" ) )

def f(x):
	if x != 0:
		return output[x-1]
	else:
		return 0

f = np.vectorize(f)
result_array = f(segments_quick)

plt.imshow(result_array)