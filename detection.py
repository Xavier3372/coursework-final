import os

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Activation, Dropout
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow_hub as hub
import numpy as np
import matplotlib.pyplot as plt
import cv2
import numpy as np

model_path = 'model/asl_model'


model = tf.keras.models.load_model('model/asl_model')
print('model loaded')
model.summary()
data_dir = 'dataset/asl_alphabet_train/asl_alphabet_train'
# getting the labels form data directory
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'nothing']

cap = cv2.VideoCapture(0)
while(True):

    _, frame = cap.read()
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 5)
    # region of intrest
    roi = frame[100:300, 100:300]
    img = cv2.resize(roi, (224, 224))

    img = img/255

    # make predication about the current frame
    prediction = model.predict(img.reshape(1, 224, 224, 3))
    char_index = np.argmax(prediction)
    # print(char_index,prediction[0,char_index]*100)

    confidence = round(prediction[0, char_index]*100, 1)
    predicted_char = labels[char_index]

    font = cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 1
    color = (0, 255, 255)
    thickness = 2

    # writing the predicted char and its confidence percentage to the frame
    msg = predicted_char + ', Conf: ' + str(confidence)+' %'
    cv2.putText(frame, msg, (80, 80), font, fontScale, color, thickness)

    cv2.imshow('frame', frame)

    # close the camera when press 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
