# Importing dependencies
import tensorflow as tf
import numpy as np
import cv2
import numpy as np

# Declare path of model
model_path = 'model/asl_model'

# Load model and save it as 'model'
model = tf.keras.models.load_model('model/asl_model')
print('model loaded')
model.summary()
data_dir = 'dataset/asl_alphabet_train/asl_alphabet_train'

# Declare detection classes
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'nothing']


def detectImg(imFrame):
    # Save cv2 image data as 'frame'
    _, frame = imFrame

    # Draw detection region on frame
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 5)

    # Save cv2 image data in detection region and resize detection region to size usable by model (224x224pixels)
    detectionRegion = frame[100:300, 100:300]
    img = cv2.resize(detectionRegion, (224, 224))

    # Normalize pixel color code from 0-255 to 0-1 to improve performance
    img = img/255

    # Run model prediction on image
    prediction = model.predict(img.reshape(1, 224, 224, 3))
    char_index = np.argmax(prediction)
    confidence = round(prediction[0, char_index]*100, 1)
    predicted_char = labels[char_index]

    # Declare cv2 text styling
    font = cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 1
    color = (0, 255, 255)
    thickness = 2

    # Add detected alphabet and confidence level to frame
    msg = predicted_char + ', Conf: ' + str(confidence)+' %'
    cv2.putText(frame, msg, (80, 80), font, fontScale, color, thickness)
    
    # Return frame and predicted character
    return frame, predicted_char
