import cv2
from sklearn import mixture
import numpy as np
import matplotlib.pyplot as plt

filePath = "C:\\Users\\Phil\\Desktop\\Sea Ice Photo for XSEDE16\\Examples\\072610_00104.jpg"
#load image
img = cv2.imread(filePath)

#create classifier
gmix = mixture.GMM(n_components=4, covariance_type='full')
#fit to image
gmix.fit(img.reshape((img.shape[0]*img.shape[1],3)))
#extract class means and cov
#this can be made to be a 'supervised' method by setting .means_ and .covars_ to mean and cov of samples
mean = gmix.means_
cov = gmix.covars_
#predict back to image
labeled_img = gmix.predict(img.reshape((img.shape[0]*img.shape[1],3))).reshape(img.shape[0],img.shape[1])
plt.imshow(labeled_img)


#Find contours and plot
contours = cv2.findContours(np.array(labeled_img,dtype="int32"),cv2.RETR_FLOODFILL,cv2.CHAIN_APPROX_SIMPLE)
imgCont = img.copy()
cv2.drawContours(imgCont, contours[0], -1, (0,255,0), 3)
plt.imshow(imgCont)

