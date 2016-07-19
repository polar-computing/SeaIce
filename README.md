# Sea Ice Imagery Classification with Machine Learning and High-Performance Computing
### XSEDE 2016 Polar Compute Hackathon - Sea Ice Team
 
Contributers: Alek Petty, Andrew Barrett, Xin Miao, Phil McDowell, Vivek Balasubramanian    

Thanks also to the Polar Research Coordination Network (RCN) hackathon organizers.

# Decription

A hot topic for the sea ice community is the segmentation and classification of sea ice imagery.

Manually delineating sea ice, open water, leads and melt ponds from sea ice images is a time consuming and labor intensive process. 

In this hackathon we developed various supervised/unsupervised training algorithms in the open source programming language Python - that read in and classify sea ice imagery. The algorithms are HPC compliant, and successful imagery analysis has been carried out on the Comet HPC. 

An interactive Python interface has been developed to allow for quick and interactive manual classification of images to drive the supervised machine learning algorithms. 

The algorithms are explained in more detail in various IPython Notebooks.

We hope to eventually use thse tools to analyze across a large number of images (across various spatial/temporal scales) to derive detailed sea ice surface parameters and their corresponding changes in time and space. 

# Code
Our original algorithm includes three major steps: (1) the image segmentation groups the neighboring pixels into objects according to the similarity of spectral and textural information; (2) a random forest classifier (RF) distinguishes four general classes: water, general submerged ice (GSI, including melt ponds and submerged ice along ice edges), shadow, and ice/snow; and (3) the polygon neighbor analysis further separates melt ponds and submerged ice from the GSI according to their spatial relationships. So far we only applied it to a rather small data set (163 aerial photographs taken during the Chinese National Arctic Research Expedition in summer 2010 (CHINARE 2010) in the Arctic Pacific Sector) due to the limited computation resources.

# Data
Data sets (all images are in JPG or TIFF format)--

Declassified GFL data (1755 images)	450 GB	The six fiducial sites and repeated images tracking data buoys/floes.
SHEBA 1998 (Perovich )	16.5 GB	Beaufort Sea, 13 flights between May 17, 1998 and October 4, 1998. Also a few National Technical Means high resolution satellite photographs.
HOTRAX 2005 (Perovich))	31.3 GB	TransArctic cruise from Alaska to Norway, 10 flights from August 14, 2005 to September 26, 2005.
CHINARE 2008 (Xie)	20.0 GB	Pacific Arctic sector (between 140 °W and 180 °W up to 86 °N), August 17 to Sept 5, 2008.
CHINARE 2010 (Xie)	23.7 GB	Pacific Arctic sector (between 150 °W and 180 °W up to 88.5 °N), July 21 to August 28, 2010
CHINARE 2012 (Xie)	21.2 GB	Transpolar section,  (Iceland to Bering Strait),  August-September 2012
The time lapse camera (Haas)	40.5 GB	Cape Joseph Henry (82.8N, -63.6W), May 2011 to July 2012.
EM-bird thickness and aerial photos (Haas)	21.2 GB	April 2009, 2011, and 2012, between 82.5 N and 86N, and -60W and -70W.
