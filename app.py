from ctypes import alignment
from re import A
import sys
import random
from textwrap import wrap
from tkinter import W
from PySide6 import QtCore, QtWidgets, QtGui
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


a = 0
translatedText = "futher"
model_path = 'model/asl_model'


model = tf.keras.models.load_model('model/asl_model')
model.summary()
data_dir = 'dataset/asl_alphabet_train/asl_alphabet_train'
# getting the labels form data directory
labels = sorted(os.listdir(data_dir))
labels[-1] = 'nothing'
print(labels)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        global translatedText

        super().__init__()
        self.setWindowTitle("Translator")

        self.setGeometry(83, 35, 1100, 700)

        self.startbutton = QtWidgets.QPushButton("Start", self)
        self.nextWord = QtWidgets.QPushButton("New Word", self)
        self.endbutton = QtWidgets.QPushButton("End", self)
        self.scr = QtWidgets.QPushButton("Screen", self)

        self.text = QtWidgets.QLabel(translatedText, self)
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
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
