#TODO create classifier class
#TODO comment + document code
#TODO enable extending classifier with mulitple images
#TODO set params as script args or config file
#TODO take optional list of class names
#TODO annotate interactive plot with instructions + current class
#TODO middle mouse click to undo previous label in interactive plot

import numpy as np
from skimage.segmentation import mark_boundaries
from skimage import measure
import matplotlib.pyplot as plt

def extractSegmentProperties(segments,img):
	# Extract feature properties
	# Mean RGB intensities
	props = measure.regionprops(segments,img[:,:,0], cache=False)
	r=[prop.mean_intensity for prop in props]
	props = measure.regionprops(segments,img[:,:,1], cache=False)
	g=[prop.mean_intensity for prop in props]
	props = measure.regionprops(segments,img[:,:,2], cache=False)
	b=[prop.mean_intensity for prop in props]
	# RGB Ratios
	Ratio1 = np.divide(np.subtract(b,r) , np.add(b,r))
	Ratio2 = np.divide(np.subtract(b,g) , np.add(b,g))
	denom = np.subtract(np.subtract(np.multiply(b,2),g),r)
	denom[denom==0] = 0.05
	Ratio3 = np.divide(np.subtract(g,r) , denom)
	# Stack properties to array
	features = np.column_stack((r,g,b,Ratio1,Ratio2,Ratio3))
	return features

def trainingSamplesRand(img,segments,features,n,preLabels = None):
	labels = []
	plt.ion()
	plt.imshow(img)
	plt.show()
	plt.draw()
	for i in xrange(n):
		# plt.ion()
		index = np.random.randint(1, features.shape[0])
		if index in segments:
			mask = np.zeros(img.shape[:2], dtype = "uint8")
			mask[segments == index] = 2
			bounded = mark_boundaries(img,mask,color=(1,1,0),mode='thick')
			plt.imshow(bounded)
			plt.draw()
			plt.pause(0.001)
			plt.show()
			labeled = False
			while not labeled:
				print "Label ", i, "of ", n
				iclass = raw_input("Enter a class (q to quit, s to skip):")
				if iclass == "q":
					return labels
				if iclass == "s":
					labeled = True
					continue
				try:
					iclass = int(iclass)
					labels.append((index,iclass))
					labeled = True
				except:
					print "Class must be an integer"
		else:
			print "Feature index out of range"
		if preLabels:
			labels = labels + preLabels
	return labels

def createTrainingSet(labels,features):
	trainingSetIndex = [x[0]-1 for x in labels]
	trainingSetClasses = [x[1] for x in labels]

	#create training set
	trainingSet = features[trainingSetIndex]

	return trainingSet,trainingSetClasses


def trainingSamplesMouse(img,segments):
	global _clickclassi
	global bounded
	labels = []
	plt.ioff()
	bounded = img.copy()
	def onclick(event):
		cm = plt.get_cmap('gist_rainbow')
		global _clickclassi
		global bounded
		if event.button == 1:
			print "clicked"
			mask = np.zeros(img.shape[:2], dtype = "uint8")
			mask[segments == segments[int(event.ydata),int(event.xdata)]] = 2
			bounded = mark_boundaries(bounded,mask,color=cm(1.*_clickclassi/10)[:3],mode='thick')
			ax.imshow(bounded)
			plt.draw()
			labels.append((segments[event.ydata,event.xdata],_clickclassi))
		if event.button == 3:
			_clickclassi += 1
	_clickclassi = 1
	fig, ax = plt.subplots()
	ax.imshow(img)
	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	plt.show(block=True)
	plt.draw()
	return labels





def reclassify(x,mapping):
	if x != 0:
		o = mapping[x-1]
		return o
	else:
		return 0

reclassify = np.vectorize(reclassify,excluded=[1])
