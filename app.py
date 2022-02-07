from ctypes import alignment
from re import A
import sys
import random
from textwrap import wrap
from tkinter import W
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
from cv2 import QRCodeDetector
from matplotlib.widgets import Widget
from autocorrect import *
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

a = 0
translatedText = "futher"

model_path = 'model/asl_model'
predicted_char = "nothing"


model = tf.keras.models.load_model('model/asl_model')
print('model loaded')
model.summary()
data_dir = 'dataset/asl_alphabet_train/asl_alphabet_train'
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
          'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'nothing', 'nothing']


class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.status:

            _, frame = self.cap.read()
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
            cv2.putText(frame, msg, (80, 80), font,
                        fontScale, color, thickness)

            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)

            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class Window(QMainWindow):
    def __init__(self):
        global translatedText

        super().__init__()
        self.setWindowTitle("Translator")

        self.setGeometry(83, 35, 1100, 700)
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        self.startbutton = QPushButton("Start", self)
        self.nextWord = QPushButton("New Word", self)
        self.endbutton = QPushButton("End", self)
        self.scr = QPushButton("Screen", self)

        self.text = QLabel(translatedText, self)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.text.move(70, 430)
        self.text.resize(1000, 100)

        self.scr.resize(800, 450)  # placeholder for screen
        self.scr.move(150, 0)

        self.endbutton.resize(100, 100)
        self.endbutton.move(850, 550)

        self.endbutton.resize(100, 100)
        self.endbutton.move(850, 550)

        self.startbutton.resize(100, 100)
        self.startbutton.move(150, 550)
        self.startbutton.setStyleSheet(
            "background-image : url(xavier_angy.jpg);")
        '''self.startbutton.setStyleSheet(
            "border-style: outset;"
            "border-radius : 50;" 
            "border-width: 10px;"
            "border-color: red;")'''

        self.nextWord.resize(100, 100)

        # self.text = QtWidgets.QLabel(
        #   "Press the button", alignment=QtCore.Qt.AlignCenter)
        '''self.layout = QtWidgets.QHBoxLayout(self) #
        self.layout.addWidget(self.startbutton)
        self.layout.addWidget(self.endbutton) '''
        self.startbutton.clicked.connect(self.startcamera)
        self.endbutton.clicked.connect(self.endcamera)
        self.nextWord.clicked.connect(self.nextword)

    def updatetext(self):
        global translatedText
        self.text.setText(translatedText)

    def camera(self):
        global a
        print(a)
        if a == 1:
            print("start")
        if a == 2:
            print("stop")

    def startcamera(self):  # what button does
        global a
        if a != 1:

            print("started")
            a = 1
            self.camera()
            self.th.start()

    def endcamera(self):
        global a
        if a == 1:
            a = 2
            print("ended")
            self.camera()

    def nextword(self):
        global translatedText
        translatedText = (autoCorrect(translatedText)[0])
        self.updatetext()

    def putwordhere(letter):
        global translatedText
        translatedText += letter


if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())
