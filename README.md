<b>Cardiovascular Abnormality Detection from Compressed ECG Signals</b><br>

This project is implemented to efficiently detect abnormal ECG segemnts from a compressed ECG signal, using Data Mining techniques. We have used Fast Co-relation based Feature Selection (fcbs) for selecting features that best describe the dataset. Further, EM Clustering has been used to segregate different ECG segements based on the selected features. 

The EM Clustering model is trained with 878 segments of ECG and is further used to classify 439 segments of ECG signal. The entire model takes 3.5 seconds to run. 
We gained 100% accuracy for training data and 88.0% average accuracy for test data.


<b>REQUIREMENTS:</b><br>
python version 2 <br>
python version 3 <br>
Packages: numpy, os, sys, math, queue, sklearn.mixture (Gaussian mixture), argparse  <br>

<b>TO RUN:</b>
1. Run chmod +x cardio.sh
2. Run sed -i -e 's/\r$//' cardio.sh
3. Run ./cardio.sh<br>

<b>RUN TIME:</b> 3.5 seconds<br><br>

<b>TRAINING DATA:</b> 878 ECG SEGMENTS <br>
<b>TESTING DATA:</b> 479 ECG SEGMENTS<br>
