# Sea Ice Imagery Classification with Machine Learning and High-Performance Computing
### XSEDE 2016 Polar Compute Hackathon - Sea Ice Team
 
Contributers: Alek Petty, Andrew Barrett, Xin Miao, Phil McDowall, Vivek Balasubramanian    

Thanks also to the Polar Research Coordination Network (RCN) hackathon organizers.

# Decription

High-resolution satellite and aerial imagery are increasingly used to provide assessments of the spatial and temporal coverage of various surface types of the Arctic and Southern Oceans. An important challenge for the sea ice community is the segmentation and classification of these images into these various surfaces (e.g. smooth ice, deformed ice, open water, melt ponds, etc). Manually delineating images can be a time consuming, and labor intensive process, however, and various tools have thus been developed to automate this process using various machine learning techniques. 

At the Extreme Science and Engineering Discovery Environment (XSEDE) 2016 conference, the Polar Research Coordination Network (RCN) organized a sea ice hackathon to unite polar scientists and high-performance computing experts in an effort to generate an open-source, machine learning toolkit to classify sea ice imagery across various sensors (aerial/satellite) and spatial scales.

# Hackathon Outcomes

We wanted to compare the computation and classification performance between:   
- Unsupervised vs. supervised classification     
- Pixel-based vs. object-based classification      
- Different classification algorithms such as GMM vs. Random Forest (and permutations thereof).   

We applied various supervised/unsupervised machine learning algorithms (mainly taken from scikit-learn/Python) to classify sea ice images. Note that an interactive Python interface has been developed to allow for quick and interactive manual classification of images to drive the supervised machine learning algorithms.

The Random forest algorithm can be easily realized in  multi-core computation system, making it very suitable to run in a high-performance computing environment. Currently, the computational challenges can be viewed in two modes:    
- Number of images that can be processed concurrently on HPC machines.      
- Optimizations at the level of individual processing functions (e.g. parallelizing the segmentation functions, classification functions) within the workflow.    

Initial evaluation of the unsupervised workflow (vanilla implementation) with images of O(10) MB of data took 30 mins of compute time on XSEDE.Comet. We expect individual image data to grow to O(1000) MB and the number of images to grow to O(100)-O(1000).

The classification/segmentation approaches are explained in more detail in various IPython Notebooks which are still being updated as the various processing chains are developed.

# Current image processing description

Our original algorithm includes three major steps:    
- The image segmentation groups the neighboring pixels into objects according to the similarity of spectral and textural information.  
- A random forest classifier (RF) distinguishes four general classes: water, general submerged ice (GSI, including melt ponds and submerged ice along ice edges), shadow, and ice/snow.        
- The polygon neighbor analysis further separates melt ponds and submerged ice from the GSI according to their spatial relationships. 

So far we only applied it to a rather small data set (aerial photographs taken during the Chinese National Arctic Research Expedition in summer 2010 (CHINARE 2010) in the Arctic Pacific Sector). We are currently testing the code on these images and other aerial/satellite imagery datasets (e.g. Operation IceBridge DMS and QuickBird)

# Hackathon conclusions and future work

Open-source Python libraries appear sufficient to produce results at least equal to those produced using commercial remote sensing image classification software, while adding more functionality, convenience and utility (at no cost). 

There are several longer-term research ideas that have been identified for future work:   
- Divide large images into small pieces to run image segmentation on multiple cores.    
- Separate meld ponds from general submerged ice using a neighbor analysis.    
- Complete the interactive sample selection approache in a service-based module, to be used in a cyberinfrastructure.    
- Replace CPU based implementations of classifiers with GPU based implementations and restructure code to take advantage of available resources.    
- Several steps in the classification proecss chain required user interaction, where Python may not be the optimum choice. These interactive components could be rewritten using a combination of Python, HTML and JavaScript ideally.   

