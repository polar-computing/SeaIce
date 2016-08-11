# TODO create classifier class
# TODO enable extending classifier with mulitple images
# TODO set params as script args or config file
# TODO take optional list of class names
# TODO annotate interactive plot with instructions + current class
# TODO middle mouse click to undo previous label in interactive plot

import matplotlib
import numpy as np
from skimage import measure
from skimage.segmentation import mark_boundaries

matplotlib.use('TkAgg')
print "Using ", matplotlib.get_backend(), " backend."
import matplotlib.pyplot as plt


def extractSegmentPropertiesRGB(segments, img):
    """Function to extract 6 properties from each segment of a segmented image.

    Returns a numpy array with 6 columns and a row per segment.
    [:,1] : Mean red (r) intensity of segment
    [:,2] : Mean green (g) intensity of segment
    [:,3] : Mean blue (b) intensity of segment
    [:,4] : (b-r)/(b+r)
    [:,5] : (b-g)/(b+g)
    [:,6] : (g-r)/(2b - g -r)

    Parameters
    ----------
    segments : ndarray, shape(M, N)
        The segmented image
    img : ndarray, shape(M, N, 3)
        The RGB image that has been segmented.


    Returns
    -------
    properties : ndarray, shape(6, n)
        A numpy array.
    """

    # Extract feature properties
    # Mean RGB intensities
    props = measure.regionprops(segments, img[:, :, 0], cache=False)
    r = [prop.mean_intensity for prop in props]
    props = measure.regionprops(segments, img[:, :, 1], cache=False)
    g = [prop.mean_intensity for prop in props]
    props = measure.regionprops(segments, img[:, :, 2], cache=False)
    b = [prop.mean_intensity for prop in props]

    # RGB Ratios
    denom = np.add(b, r)
    denom[denom == 0] = 0.05
    Ratio1 = np.divide(np.subtract(b, r), denom)

    denom = np.add(b, g)
    denom[denom == 0] = 0.05
    Ratio2 = np.divide(np.subtract(b, g), denom)

    denom = np.subtract(np.subtract(np.multiply(b, 2), g), r)
    denom[denom == 0] = 0.05
    Ratio3 = np.divide(np.subtract(g, r), denom)

    # Stack properties to array
    properties = np.column_stack((r, g, b, Ratio1, Ratio2, Ratio3))

    return properties


def createTrainingSet(labels, features):
    """Function to create a training set from segment properties after labeling.

    Subsets features to those which are in 'labels' and returns a tuple of properties and corresponding labels.


    Parameters
    ----------
    labels : ndarray, shape(n, 2)
        Each row contains a class label and corresponding segment index
    properties : ndarray, shape(N, 6)
        Each row corresponds to a segment and contains 6 properties of the segment. Ordered by segment index.


    Returns
    -------
    trainingSet,trainingSetClasses : tuple
        A tuple containing a subset of properties (ndarray, shape(n, 6)) and a list of corresponding segment index
    """

    # seperate labels into class and segment index
    trainingSetIndex = [x[0] - 1 for x in labels]
    trainingSetClasses = [x[1] for x in labels]

    # create training set
    trainingSet = features[trainingSetIndex]

    return trainingSet, trainingSetClasses


def trainingSamplesMouse(img, segments, maxClasses=3, iclasses=None):
    """Function to interactively label segments with a class

    This function displays the image and waits for mouse clicks. A left mouse button click will label a segment,
    and display a colored polygon around that segment. A right mouse button click will increment the class.
    Class labels are integers between 1 and maxClasses. Alternatively a list of class names may be passed as iclasses.
    In this case maxClasses is ignored. Returns an array containing the segment index and assigned class label.


    Parameters
    ----------
    img : ndarray, shape(M, N, 3)
        The RGB image that has been segmented.
    segments : ndarray, shape(M, N)
        The segmented image.
    maxClasses: int
        The number of classes which the image will be labeled with.
        Default - 3
    iclasses:
        An (optional) list of class names to label the image with.
        Overrides maxClasses with len(iclasses)


    Returns
    -------
    labels : ndarray, shape(n, 2)
        An array containing segment index and associated class label
    """
    # Globals to get around limitations of 2.7 closures
    global _clickclassi
    global bounded
    global _txt

    # Check for named classes
    if not iclasses:
        iclasses = range(0, maxClasses)
    else:
        maxClasses = len(iclasses)

    # Create list to store output
    labels = []

    # Turn interactive mode off so plot is blocking
    plt.ioff()

    # Copy original image into global
    bounded = img.copy()

    # Set up plot labels and color map
    labelText = "Current class: "
    cm = plt.get_cmap('gist_rainbow')

    # Call back function executed on mouseclick on figure
    def onclick(event):
        # globals again
        global _clickclassi
        global bounded
        global _txt

        # If left mouse button click
        if event.button == 1:
            # calculate color for class
            color = cm(int(_clickclassi * (256.0 / maxClasses)))[:3]
            # create mask containing only selected segment
            mask = np.zeros(img.shape[:2], dtype="uint8")
            mask[segments == segments[int(event.ydata), int(event.xdata)]] = 2
            # Highlight segment on image and display
            bounded = mark_boundaries(bounded, mask, color=color, mode='thick')
            ax.imshow(bounded)
            plt.draw()
            # Add segment index and class to labels
            labels.append((segments[int(event.ydata), int(event.xdata)], _clickclassi))
        # If right mouse button click
        if event.button == 3:
            # Cycle through classes
            _clickclassi = (_clickclassi + 1) % maxClasses
            # Clear plot and redraw to get rid of existing text labels
            plt.cla()
            ax.imshow(bounded)
            _txt = plt.text(0, -20, labelText + str(iclasses[_clickclassi]))
            plt.draw()

    # Set up initial class and image
    _clickclassi = 0
    fig, ax = plt.subplots()
    ax.imshow(img)
    _txt = plt.text(0, -20, labelText + str(iclasses[_clickclassi]))
    # Attach callback function to figure and draw
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show(block=True)

    # Returns when figure closed
    return labels

#TODO replace with skimage native map function
def reclassify(x, mapping):
    """Function to reclassify an int raster to a mapping

    Parameters
    ----------
    x : int
        The integer pixel value to be reclassified
    mapping: list[int]
        New mapping of pixel values. newvalue = mapping[x]


    Returns
    -------
    o : int
        New class for pixel
    """
    if x != 0:
        o = mapping[x - 1]
        return o
    else:
        return 0


"""Vectorized version of reclassify to apply to np array"""
reclassify = np.vectorize(reclassify, excluded=[1])


