# SST Coursework 2022

## About the app

<p>A python application that utilises the tensorflow object detection algorithm to achieve automatic detection of american sign language gestures.</p>
<br/>
<p>Disclaimer: This is a <b>prototype</b> machine learning app built on a <b>limited</b> dataset, we are unable to guarantee 100% accuracy in the detection of hand gestures</p>
<br/>
<p> This app was created to allow for the more seamless integration of communication through american sign language(asl) into our daily lives through the use of machine learning in order to construct a realtime asl translator in python. The translator features autocorrect features, as well as an intuitive gui to help with the usage of the app.</p>
<br/>
<p> The app utilises a machine learning model that was trained through transfer learning with pre-trained object detection models from the tensorflow model garden. The tensorflow object detection library is utilised to allow for the real time detection of hand gestures from the webcam. Jupyter notebooks used for dataset collection and model training can  be found under the Training programs folder in Tensorflow/workspace. All reference material used during the creation of this projects can be found in the credits section below. The dataset used for the trainig of the tensorflow model can be found [here](https://drive.google.com/drive/folders/1bFOTeoUWdaG37eiMCa2sYimpsN4JxU3f?usp=sharing).</p>


## Installation Steps

<br />
<b>Step 1.</b> Clone this repository: https://github.com/Xavier3372/coursework-final
<br/><br/>
<b>Step 2.</b> Open a new terminal window and cd into the program directory
<pre>
# In a new terminal window
cd {your program directory here}
</pre>
<b>Step 3.</b> Create a virtual environment
<pre>
pip install virtualenv
virtualenv venv 
</pre>
<br/>
<b>Step 4.</b> Activate the virtual environment
<pre>
source venv/bin/activate # Mac
.\venv\Scripts\activate # Windows 
</pre>
<b>Step 5.</b> Install dependencies
<pre>
pip install cython numpy six
pip install -r requirements.txt 
</pre>
<br/>
<b>Step 6.</b> Deactivate the virtual environment
<pre>
deactivate
</pre>
<br/>
<b>Step 7.</b> Install Protobuf
<pre>
brew install protobuf
</pre>
<br/>
<b>Step 8.</b> clone tensorflow object detection library
<pre>
git clone https://github.com/tensorflow/models
</pre>
<br/>
<b>Step 9.</b> Activate the venv
<pre>
source venv/bin/activate # Mac
.\venv\Scripts\activate # Windows 
</pre>
<br/>
<b>Step 10.</b> Install the tensorflow object detection library
<pre>
cd models/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . && python -m pip install .
</pre>
<br/>
<b>Step 11.</b> Run the app
<pre>
python3 app.py
</pre>

## Credits
### Contributers
<p> Below is a list of contributers who helped with the creation of this project </p>
<br/>
<b>[Jovan Ang](https://github.com/DudeNav0J)</b>
<br/>
<b>[Jerald Tee](https://github.com/jeraldtea)</b>
<br/>
<b>[Xavier Koh](https://github.com/Xavier3372)</b>
</br>
### References
<p> Below is a list of websites, videos and repositories referenced and used in the creation of this project </p>
