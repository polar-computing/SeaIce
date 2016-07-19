from skimage.segmentation import quickshift, mark_boundaries
from skimage import feature
import skimage
import cv2

filePath = "C:\\Users\\Phil\\Desktop\\Sea Ice Photo for XSEDE16\\examples\\072610_00104.jpg"

img = cv2.imread(filePath)

out = quickshift(img)

def maskSuperPixel(superPix,index,image):
	mask = np.zeros(img.shape[:2], dtype = "uint8")
	mask[superPix == index] = 255
	cv2.imshow("", cv2.bitwise_and(image, image, mask = mask))
	cv2.waitKey(0)

props = skimage.measure.regionprops(out,img[:,:,0], cache=False)
r=[prop.mean_intensity for prop in props]
props = skimage.measure.regionprops(out,img[:,:,1], cache=False)
g=[prop.mean_intensity for prop in props]
props = skimage.measure.regionprops(out,img[:,:,2], cache=False)
b=[prop.mean_intensity for prop in props]
brRatio = np.divide(b,r)
bgRatio = np.divide(b,g)
grRatio = np.divide(g,r)
samples = np.column_stack((r,g,b,brRatio,bgRatio,grRatio))