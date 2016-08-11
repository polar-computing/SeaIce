"""
Train random forest classifier on multiple images
Usage: python train_classifier_multi.py -d <directory of images> -o <OPTIONAL: directory to save classifier>
e.g. python train_classifier_multi.py -d C:\trainingImages -o c:\trainingImages\classifier

Images should be .jpg

Segments images sequentially and creates interactive window to label segments
Left click to label with current class
Right click to increment current class
Close window to move to next image

Saves trained classifier as fittedforest.p in directory specified by option -o.
If -o not set, saves to inputDirectory
"""

from sklearn.ensemble import RandomForestClassifier
from skimage.segmentation import quickshift
from scipy import misc
from segmentUtils import *
import pickle
import argparse
import os
from datetime import datetime
import ConfigParser

parser = argparse.ArgumentParser(description="Quicksift + random forest image classification")
parser.add_argument("-d", "--inputDirectory", help="Path to images to classify'", required=True)
parser.add_argument("-o", "--outputDirectory", help="Path to store classifier'")

args = parser.parse_args()

config = ConfigParser.ConfigParser()
cf = config.read('ClassifierConfig.ini')
if len(cf)<1:
    print "Configuration file not found. Reverting to defaults."
    qs_kernel_size = 5
    qs_max_dist = 5
    qs_ratio = 0.5
else:
    qs_kernel_size = int(config.get('QuickShift', 'qs_kernel_size'))
    qs_max_dist = int(config.get('QuickShift', 'qs_max_dist'))
    qs_ratio = float(config.get('QuickShift', 'qs_ratio'))
print "Quickshift kernel_size = %s \nQuickshift max_dist = %s \nQuickshift ratio = %s"%(qs_kernel_size, qs_max_dist,qs_ratio )
# # Training Samples parameters
# TSn = 20

# Random forest parameters
RF_n_estimators = 100

validFileExt = (".jpg",".JPG",".tif")

trainDir = args.inputDirectory
images = [file for file in os.listdir(trainDir) if file.endswith(validFileExt)]

if len(images) < 1:
    raise IOError("No supported file formats found")


trainingSet = []
trainingSetClasses = []

for filePath in images:
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Loading ", filePath
    img = misc.imread(trainDir + "\\" + filePath)[:,:,:3]
    print "Image loaded. ", img.shape[0], " x ", img.shape[1]
    print "Segmenting..."
    t1 = datetime.now()
    segments = quickshift(img, kernel_size=qs_kernel_size, max_dist=qs_max_dist, ratio=qs_ratio)
    t2 = datetime.now()
    delta = t2 - t1
    seconds = delta.total_seconds()
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print "Segmentation complete in %d:%02d:%02d" % (h, m, s)
    print("Quickshift number of segments: %d" % len(np.unique(segments)))
    features = extractSegmentPropertiesRGB(segments,img)
    # Interactively label image
    labels = trainingSamplesMouse(img,segments,maxClasses=5)
    # Create trainingset
    trainingSet_, trainingSetClasses_ = createTrainingSet(labels,features)
    if len(trainingSet) > 0:
        trainingSet = np.row_stack((trainingSet,trainingSet_))
        trainingSetClasses = trainingSetClasses + trainingSetClasses_
    else:
        trainingSet = trainingSet_
        trainingSetClasses = trainingSetClasses_

forest = RandomForestClassifier(n_estimators = RF_n_estimators)
forest = forest.fit(trainingSet,trainingSetClasses)

if args.outputDirectory:
    if not os.path.exists(args.outputDirectory):
        os.makedirs(args.outputDirectory)
    pickle.dump(forest, open(args.outputDirectory + "\\fittedforest.p", "wb"))
else:
    pickle.dump(forest, open(args.inputDirectory + "\\fittedforest.p", "wb"))