
# ## Sea ice classification with GMM (pixel based) - unsupervised
# IPython notebook demo of the Gaussian Mixture Model (GMM) algorithm for sea ice classification (pixel based)
# As part of the 2016 XSEDE Polar Hackathon. 
# 
# Contributing authors: Alek Petty, Andrew Barrett, Xin Miao, Phil McDowell, Vivek Balasubramanian

from scipy import misc
from pylab import *
from skimage.segmentation import mark_boundaries
#load and apply the Gaussian Mixture Model (GMM) classification scheme to one sea ice image.
from sklearn import mixture
from glob import glob

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

def getMultiImages(trainingPath, numFiles):
    # Read in multiple images
    # Number of images we want to use from within the training directory 
    files=glob(trainingPath+'*.jpg')
    imgAll = misc.imread(files[0]).reshape((-1, 3))
    print 'Num of files used: '+str(numFiles)+'/'+str(size(files))
    iterfiles = iter(files)
    next(iterfiles)

    # Concatenate images into one big image
    for file in files[0:numFiles]:
        imgT = misc.imread(file).reshape((-1, 3))
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

trainingPath="../../../DATA/IMAGERY/XIN/TRAINING/"
filePath = "../../../DATA/IMAGERY/XIN/"

numTrainingImages=3
iceTypes=4
imageName="072610_00211.jpg"

# Read in a sea ice image
img = misc.imread(filePath+imageName)
plotImage(img, imageName)

# Train the algorithm (GMM) with a number of images 
#First generate a large image from multiple images
imgAll = getMultiImages(trainingPath, numTrainingImages)

gmixAll = mixture.GMM(n_components=iceTypes, covariance_type='full')
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

plotLabel(img, labeledImg, outStr=str(numTrainingImages)+'trainingImages')



