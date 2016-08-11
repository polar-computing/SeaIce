"""
Classify images based on pre-trained random forest classifier
Usage: python classify.py -c <Full path to classifier> -d <directory of images>
e.g. python train_classifier_multi.py -c C:\testImages\classifier\fittedforest.p -d C:\testImages

Images should be .jpg

Segments images sequentially and classifies
Classified images are saved in a subdirectory of the input folder
"""


from sklearn.ensemble import RandomForestClassifier
from skimage.segmentation import quickshift
from scipy import misc
from segmentUtils import *
import pickle
import argparse
import os
from datetime import datetime


def timeDeltaToHMS(timeDelta):
    seconds = timeDelta.total_seconds()
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return (h, m, s)

parser = argparse.ArgumentParser(description="Quicksift + random forest image classification")
parser.add_argument("-c", "--classifier", help="Optional: Trained Classifier. If argument not set will look for 'fittedforest.p in input directory'")
parser.add_argument("-d", "--directory", help="Path to images to classify'", required=True)
parser.add_argument("-s", "--savesegs", help="Optional: Boolean; save segmented image'")

args = parser.parse_args()

os.chdir(args.directory)

if args.classifier:
    try:
        forest = pickle.load( open(args.classifier, "rb") )
        print "Classifier loaded..."
    except IOError:
        print "Classifier not found. Exiting..."
        quit()
else:
    try:
        forest = pickle.load( open("fittedforest.p", "rb") )
        print "Classifier loaded..."
        print
    except IOError:
        print "Default classifier not found. Exiting..."
        quit()



validFileTypes = (".jpg",".JPG")
files = os.listdir(".")
images = [file for file in files if file.endswith(validFileTypes)]

if len(images) < 1:
    print "No images found."
    quit()

if args.savesegs:
    if not os.path.exists("segmented"):
        os.makedirs("segmented")

if not os.path.exists("classified"):
    os.makedirs("classified")

qs_kernel_size = 7
qs_max_dist = 5
qs_ratio = 0.5


for imgPath in images:
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    print "Loading ", imgPath
    img = misc.imread(imgPath)[:,:,:3]
    print "Image loaded. ", img.shape[0], " x ", img.shape[1]
    print "Segmenting..."
    t1 = datetime.now()
    segments = quickshift(img, kernel_size=qs_kernel_size, max_dist=qs_max_dist, ratio=qs_ratio)
    t2 = datetime.now()
    delta = t2 - t1
    print "Segmentation complete in %d:%02d:%02d" % timeDeltaToHMS(delta)
    features = extractSegmentPropertiesRGB(segments,img)
    print "Classifying..."
    output = forest.predict(features)
    result = reclassify(segments, output)

    if args.savesegs:
        print "Saving segmented image..."
        misc.imsave("segmented\\" + imgPath, segments)

    print "Saving classified image..."
    misc.imsave("classified\\" + imgPath, result)

