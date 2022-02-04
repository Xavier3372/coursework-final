# SST Coursework 2022

<p>A python application that utilises the tensorflow object detection algorithm to achieve automatic detection of american sign language gestures.</p>

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
<b>Step 10.</b> Build the tensorflow object detection library
<pre>
cd models/research && protoc object_detection/protos/*.proto --python_out=. && cp object_detection/packages/tf2/setup.py . && python -m pip install .
</pre>
<br/>
<b>Step 11.</b> Run the app
<pre>
python3 app.py
</pre>