import numpy as np
from osgeo import gdal, osr
import datetime as dt
import matplotlib.pyplot as plt
#import pylab

# Extracts the coordinates of an image in the native projection and
# returns a 2D arrays of these coordinates.
def GetImageLocation(fili, corner=True):

    # Defines pixel offset if image corners are
    # requested
    if (corner == True):
        xshift = 0.5
        yshift = 0.5
    else:
        xshift = 0.0
        yshift = 0.0

    # Open file
    ds = gdal.Open(fili)

    # Get image projection
    proj = ds.GetProjection()

    # Define WGS84 Platte Caree
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
           SPHEROID["WGS 84",6378137,298.257223563,
               AUTHORITY["EPSG","7030"]],
           AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
           AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
           AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""

    # Get location and size of image
    width = ds.RasterXSize
    height = ds.RasterYSize
    gt = ds.GetGeoTransform()

    # Calculate corners of image

    # Calculate center of image
    cntx = gt[0]+(gt[1]*width*0.5)
    cnty = gt[3]+(gt[5]*height*0.5)

    # Put coordinates into some structure

    # Generate projection tranformation
    inproj = osr.SpatialReference()
    inproj.ImportFromWkt(proj)

    outproj = osr.SpatialReference()
    outproj.ImportFromWkt(wgs84_wkt)

    transform = osr.CoordinateTransformation(inproj,outproj)

    lon, lat, elev = transform.TransformPoint(cntx,cnty)

    # Return structure
    return lat, lon


# Gets timestamp for image acquistition from filename
def GetImageTimeStamp(fili):

    timestamp = fili.split("_")[1]
    dates = dt.datetime.strptime(timestamp,'%Y%m%d%H%M%S')

    return dates


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

# Plot a QuickBird RGB image
def PlotQBirdImage(filein, fileout, figsize=(5,5)):

    rgb = GetQBirdRGB(filein)

    rgb = np.ma.masked_where(rgb<1,rgb)

    image = (0.299*rgb[:,:,0] + 0.587*rgb[:,:,1] + 0.114*rgb[:,:,2])

    fig = plt.figure(figsize=(5,5))
    #ax=gca()
    im2 = plt.imshow(QBIRD, vmin = 0, vmax = 255, cmap = cm.gist_gray, rasterized=True)
    plt.subplots_adjust(bottom=0.09, left=0.11, top = 0.94, right=0.99, hspace=0.22)
    plt.savefig(fileout, dpi=300)
    fig.close()

    return






