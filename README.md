# SeaIce
Deriving sea ice concentration, floe size, and melt pond distributions through object-based image classification algorithms based on high spatial resolution sea ice images (HRI). 

# Decription
We expect to use a large number of HRI for deriving detailed sea ice concentration, floe size, and melt pond distributions over wider regions, and extracting sea ice physical parameters and their corresponding changes between years. Manually delineating sea ice and melt ponds is time-consuming and labor-intensive. We propose to develop a HPDC version of object-based image classification algorithm as a cyberinfrastructrure (CI) module, so that the interoperability can be realized not only at the data exchange and Web services level, but at the knowledge or product level.

# Code
Our original algorithm includes three major steps: (1) the image segmentation groups the neighboring pixels into objects according to the similarity of spectral and textural information; (2) a random forest classifier (RF) distinguishes four general classes: water, general submerged ice (GSI, including melt ponds and submerged ice along ice edges), shadow, and ice/snow; and (3) the polygon neighbor analysis further separates melt ponds and submerged ice from the GSI according to their spatial relationships. So far we only applied it to a rather small data set (163 aerial photographs taken during the Chinese National Arctic Research Expedition in summer 2010 (CHINARE 2010) in the Arctic Pacific Sector) due to the limited computation resources.

# Data
## Input data:


# Tools
Potential tools/languages to be used: Python, QGIS, matlab, idl, ArcGIS
