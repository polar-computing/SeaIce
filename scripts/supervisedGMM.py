import cv2
from sklearn import mixture
import numpy as np
import os

#########################
#Double click to set vertices of sample polygon
#Space bar to store sample, enter name for class
#'esc' key to end sampling
#########################

filePath = "C:\\Users\\Phil\\Desktop\\Sea Ice Photo for XSEDE16\\Examples\\072610_00104.jpg"
#load image
img = cv2.imread(filePath)

class PixelClass:
    def __init__(self,name,samples=None):
        self.name = name
        self.samples = []
        self.mean = None
        self.cov = None
        self.count=len(samples)
        if samples:
            self.add_samples(samples)
    def add_samples(self,samples):
        self.samples = self.samples + samples
        self.mean = np.mean(self.samples, axis=0)
        self.cov = np.cov(self.samples, rowvar=0)
        self.count = len(self.samples)

class ClassLibrary:
    def __init__(self):
        self.classes = {}
        self.k = len(self.classes)
        self.sensors = set()
        self.img = None
    def add_samples(self,iclass,samples):
        if iclass in self.classes:
            self.classes[iclass].add_samples(samples)
            print "Updating class [" + iclass + "] with " + str(len(samples)) + " samples"
        else:
            print "Creating class [" + iclass + "] with " + str(len(samples)) + " samples"
            self.classes[iclass] = PixelClass(iclass,samples)
        self.k = len(self.classes)
    def supervisedSelection(self,filePath):
        #Ask for filename, loop until valid file
        if not os.path.isfile(filePath):
            print 'File Not Found'
            return -1
        #Load image from filepath

        pts = []

        def draw_polygon(event,x,y,flags,param):
            if event == cv2.EVENT_LBUTTONDBLCLK:
                cv2.circle(imgOverlay,(x,y),5,(255,0,0),-1)
                pts.append((x,y))

        img = cv2.imread(filePath)
        self.img = img
        imgOverlay = img.copy()
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('image',draw_polygon)
        while(1):
            cv2.imshow('image',imgOverlay)
            key = cv2.waitKey(20) & 0xFF
            if key == 27:
                break
            if key == 32:
                cv2.destroyAllWindows()
                name = raw_input("Set Class")
                mask = np.zeros(img.shape, dtype=np.uint8)
                roi_corners = np.array([pts], dtype=np.int32)
                    # fill the ROI so it doesn't get wiped out when the mask is applied
                channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
                ignore_mask_color = (255,)*channel_count
                cv2.fillPoly(mask, roi_corners, ignore_mask_color)
                masked_image = cv2.bitwise_and(img, mask)
                plt.imshow(masked_image)
                index = masked_image.nonzero()
                pixels = []
                pts = []
                for i in range(len(index[0])):
                    x=index[0][i]
                    y=index[1][i]
                    r=img[x,y,0]
                    g=img[x,y,1]
                    b=img[x,y,2]
                    pixels.append([r,g,b])
                self.add_samples(name,pixels)
                cv2.namedWindow('image')
                cv2.setMouseCallback('image',draw_polygon)
        cv2.destroyAllWindows()
    def summary(self):
        print ""
        for i in self.classes:
            print i + " :  " + str(self.classes[i].count) + " pixels  ||"
            print i + " Mean :  " + str(self.classes[i].mean)
            print i + " Cov :  " + str(self.classes[i].cov)
            print "#####################################################"
        return 1
    def outputClasses(self):
        means = []
        covars = []
        for key, value in self.classes.iteritems():
            means.append(value.mean.tolist())
            covars.append(value.cov.tolist())
        return np.array(means),np.array(covars)
    def __repr__(self):
        print ""
        for i in self.classes:
            print i + " :  " + str(self.classes[i].count) + " pixels"
        return "+++++++++++++++++++++++++++"

lib = ClassLibrary()
lib.supervisedSelection(filePath)
means,covars = lib.outputClasses()



gmix = mixture.GMM(n_components=lib.k, covariance_type='full')
gmix.means_=means
gmix.covars_=covars
labeled_img = gmix.predict(img.reshape((img.shape[0]*img.shape[1],3))).reshape(img.shape[0],img.shape[1])
labeled_img=np.array(labeled_img,dtype="int32")
plt.imshow(labeled_img)
