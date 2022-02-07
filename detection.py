import tensorflow as tf
import numpy as np
import cv2
import numpy as np

model_path = 'model/asl_model'


model = tf.keras.models.load_model('model/asl_model')
print('model loaded')
model.summary()
data_dir = 'dataset/asl_alphabet_train/asl_alphabet_train'
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'nothing']


def detectTest():
    cap = cv2.VideoCapture(0)
    while(True):

        _, frame = cap.read()
        cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 5)

        roi = frame[100:300, 100:300]
        img = cv2.resize(roi, (224, 224))

        img = img/255

        prediction = model.predict(img.reshape(1, 224, 224, 3))
        char_index = np.argmax(prediction)

        confidence = round(prediction[0, char_index]*100, 1)
        predicted_char = labels[char_index]

        font = cv2.FONT_HERSHEY_TRIPLEX
        fontScale = 1
        color = (0, 255, 255)
        thickness = 2

        msg = predicted_char + ', Conf: ' + str(confidence)+' %'
        cv2.putText(frame, msg, (80, 80), font, fontScale, color, thickness)

        cv2.imshow('frame', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def detectImg():
    cap = cv2.VideoCapture(0)

    frame = cap.read()
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 5)

    roi = frame[100:300, 100:300]
    img = cv2.resize(roi, (224, 224))

    img = img/255

    prediction = model.predict(img.reshape(1, 224, 224, 3))
    char_index = np.argmax(prediction)

    confidence = round(prediction[0, char_index]*100, 1)
    predicted_char = labels[char_index]

    font = cv2.FONT_HERSHEY_TRIPLEX
    fontScale = 1
    color = (0, 255, 255)
    thickness = 2

    msg = predicted_char + ', Conf: ' + str(confidence)+' %'
    cv2.putText(frame, msg, (80, 80), font, fontScale, color, thickness)
    return frame, predicted_char


detectTest()
