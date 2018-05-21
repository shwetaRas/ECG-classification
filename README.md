Cardiovascular Abnormality Detection from Compressed ECG Signals

This project is implemented to efficiently detect abnormal ECG segemnts from a compressed ECG signal, using Data Mining techniques. We have used Fast Co-relation based Feature Selection (fcbs) for selecting features that best describe the dataset. Further, EM Clstering has been used to segregate different ECG segements based on the selected features. 

The EM Clustering model is trained with 878 segments of ECG and is further used to classify 439 segments of ECG signal. The entire model takes 3.5 seconds to run. 
We gained 100% accuracy for training data and 88.0% average accuracy for test data.


REQUIREMENTS:
python version 2 
python version 3
Packages: numpy, os, sys, math, queue, sklearn.mixture (Gaussian mixture), argparse  

TO RUN:
1. Navigate into the DM_Final_Project floder
2. Run chmod +x cardio.sh
3. Run sed -i -e 's/\r$//' cardio.sh
4. Run ./cardio.sh

RUN TIME: 3.5 seconds

TRAINING DATA: 878 ECG SEGMENTS 
TESTING DATA: 479 ECG SEGMENTS
