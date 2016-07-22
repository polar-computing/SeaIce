
# ## Sea ice classification with GMM (pixel based) - unsupervised
# IPython notebook demo of the Gaussian Mixture Model (GMM) algorithm for sea ice classification (pixel based)
# As part of the 2016 XSEDE Polar Hackathon. 
# 
# Contributing authors: Alek Petty, Andrew Barrett, Xin Miao, Phil McDowell, Vivek Balasubramanian


## Please note that dependent software packages are currently installed in /home/02374/vivek91. Once stabilized 
## will create specific modules for them.

import matplotlib

matplotlib.use("AGG")       # Just to tell the imshow() function not to write to DISPLAY but to the buffer

from scipy import misc
from pylab import *
from skimage.segmentation import mark_boundaries
#load and apply the Gaussian Mixture Model (GMM) classification scheme to one sea ice image.
from sklearn import mixture
from glob import glob
from osgeo import gdal
import re
import os, argparse

def sortGMM(gmixT):
	# Sort the classification by mean spectral values 
	# For consistency with later classifications
	sort_indices = gmixT.means_.argsort(axis = 0)
	order = sort_indices[:, 0]
	#print('\norder:', order)
	gmixT.means_ = gmixT.means_[order,:]    
	gmixT.covars_ = gmixT.covars_[order, :]
	a=[gmixT.weights_[x] for x in order]
	gmixT.weights_=a
	return gmixT

def plotImage(img, imageName):
	fig6 = figure(figsize=(7, 6))
	xlabel('x')
	ylabel('y')
	imshow(img)
	title(imageName)
	#plt.show()
	savefig('./Out'+imageName)

# Reads r, g, b from a QuckBird GeoTiff
def GetQBirdRGB(fili):

	geo = gdal.Open(fili)

	nx = geo.RasterXSize
	ny = geo.RasterYSize
	 
	band1 = geo.GetRasterBand(1)  # Blue
	band2 = geo.GetRasterBand(2)  # Green
	band3 = geo.GetRasterBand(3)  # Red

	b = band1.ReadAsArray()
	g = band2.ReadAsArray()
	r = band3.ReadAsArray()

	cube = np.empty([ny,nx,3], dtype=b.dtype)
	cube[:,:,0] = r
	cube[:,:,1] = g
	cube[:,:,2] = b

	return cube

def getImage(fili, flatten=False):

	if (re.search("\.jpg$",fili)):
		img = misc.imread(fili)
	elif (re.search("\.tif$",fili)):
		img = GetQBirdRGB(fili)
	else:
		print "% getImage: Reader for filetype not available"
		
	if (flatten):
		img.reshape((-1,3))
		
	return img
	
def getMultiImages(trainingPath, numFiles, filetype='jpg'):
	# Read in multiple images
	# Number of images we want to use from within the training directory 
	files=glob(trainingPath+'*.'+filetype)
	imgAll = getImage(files[0], flatten=True)
	print 'Num of files used: '+str(numFiles)+'/'+str(size(files))

	# Concatenate images into one big image
	for file in files[1:numFiles]:
		imgT = getImage(file, flatten=True)
		imgAll=np.concatenate((imgT, imgAll))
	print 'size of combined image:', imgAll.shape

	return imgAll

def plotLabel(img, labeledImgT, outStr=''):
	fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'}, 
							figsize=(14, 6))
	ax[0].imshow(mark_boundaries(img, labeledImgT))
	ax[1].imshow(labeledImgT, cmap=cm.cubehelix)
	ax[0].set_title("Classification based on training set of multiple images")
	for a in ax:
		a.set_xticks(())
		a.set_yticks(())
	plt.savefig('./labelledImage'+outStr+'.png')


if __name__ == "__main__":

	#trainingPath="../../../DATA/IMAGERY/XIN/TRAINING/"
	#filePath = "../../../DATA/IMAGERY/XIN/"
	#imageName="072610_00211.jpg"
	#numTrainingImages=3
	#iceTypes=4

	parser = argparse.ArgumentParser()
	parser.add_argument('--imagepath', help='path to file to be classified')
	parser.add_argument('--trainingpath', help="path to folder containing training images")
	parser.add_argument('--num_train', help="number of training images to be used from specified path")
	parser.add_argument('--icetypes', help='number of classifiers')

	args = parser.parse_args()

	# Read in a sea ice image
	img = getImage(args.imagepath)
	#plotImage(img, imageName)

	# Train the algorithm (GMM) with a number of images 
	#First generate a large image from multiple images
	imgAll = getMultiImages(args.trainingpath, args.num_train, filetype=os.path.basename(args.imagepath).split('.')[1])

	gmixAll = mixture.GMM(n_components=args.icetypes, covariance_type='full')
	gmixAll.fit(imgAll)
	#extract class means and cov
	#this can be made a 'supervised' method by setting .means_ and .covars_ to mean/cov of samples
	#mean = gmixAll.means_
	#cov = gmixAll.covars_

	# Sort indices of GMM in ascending order
	gmixAll=sortGMM(gmixAll)
	#gmixAll.means_

	#predict labels based on training set
	labeledImg = gmixAll.predict(img.reshape((-1,3))).reshape(img.shape[0],img.shape[1])

	plotLabel(img, labeledImg, outStr=str(args.num_train)+'trainingImages')



