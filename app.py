from ctypes import alignment
from re import A
from signal import signal
import sys
from textwrap import wrap
from tkinter import W
from turtle import right
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
import tensorflow as tf
import numpy as np
import autocorrect as ac
import detection as dt


from cv2 import QRCodeDetector
from matplotlib.widgets import Widget
import os
import time

import cv2


class ImageThread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.cap = True

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.status:
            frame = dt.detectImg(self.cap.read(0))[0]
            # _, frame = self.cap.read()
            # cv2.rectangle(frame, (100, 100), (300, 300), (0, 0, 255), 5)

            # roi = frame[100:300, 100:300]
            # img = cv2.resize(roi, (224, 224))

            # img = img/255

            # prediction = model.predict(img.reshape(1, 224, 224, 3))
            # char_index = np.argmax(prediction)

            # confidence = round(prediction[0, char_index]*100, 1)
            # predicted_char = labels[char_index]

            # font = cv2.FONT_HERSHEY_TRIPLEX
            # fontScale = 1
            # color = (0, 255, 255)
            # thickness = 2

            # msg = predicted_char + ', Conf: ' + str(confidence)+' %'
            # cv2.putText(frame, msg, (80, 80), font,
            #             fontScale, color, thickness)

            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(960, 540, Qt.KeepAspectRatio)

            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class UpdateThread(QThread):
    updateLabel = Signal()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.prevChar = 'nothing'
        self.prevchangetime = time.time()

    def run(self):
        print("thread running")
        self.cap = cv2.VideoCapture(0)
        while True:
            self.currenttime = time.time()
            self.predicted_char = dt.detectImg(self.cap.read())[1]
            if self.predicted_char != self.prevChar:
                self.prevchangetime = time.time()
                self.prevChar = self.predicted_char
            if self.currenttime - self.prevchangetime >= 1 and self.predicted_char != 'nothing':
                self.prevchangetime = time.time()
                self.updateLabel.emmit(self.predicted_char)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Title and dimensions
        self.setWindowTitle("ASL Recognition")
        self.setGeometry(0, 0, 800, 500)

        # Create a label for the display camera
        self.displayLabel = QLabel(self)
        self.displayLabel.setFixedSize(960, 540)

        # Declare variables
        self.currentWord = ""
        self.sentence = ""

        # Thread in charge of updating the image
        self.ith = ImageThread(self)
        self.ith.updateFrame.connect(self.setImage)

        # Thread in charge of when to update the translated text label
        self.uth = UpdateThread(self)
        self.uth.updateLabel.connect(self.updateText)
        self.uth.start()

        # Labels layout
        self.translatedLabel = QLabel()
        self.translatedLabel.setWordWrap(True)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.spaceButton = QPushButton("Next Word")
        self.backspaceButton = QPushButton("Backspace")
        self.resetButton = QPushButton("Reset")
        self.spaceButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.backspaceButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.resetButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.spaceButton)
        buttons_layout.addWidget(self.backspaceButton)
        buttons_layout.addWidget(self.resetButton)

        bottomLayout = QHBoxLayout()
        bottomLayout.addLayout(buttons_layout, 1)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.displayLabel)
        layout.addWidget(self.translatedLabel)
        layout.addLayout(bottomLayout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connections
        self.start()
        self.resetButton.clicked.connect(self.reset)
        self.backspaceButton.clicked.connect(self.backspace)
        self.spaceButton.clicked.connect(self.space)

    @Slot()
    def start(self):
        print("Starting...")
        self.ith.start()

    @Slot(QImage)
    def setImage(self, image):
        self.displayLabel.setPixmap(QPixmap.fromImage(image))

    @Slot()
    def updateText(self, nextchar):
        self.currentWord += nextchar
        self.translatedLabel.setText(self.sentence + " " + self.currentWord)

    @Slot()
    def reset(self):
        self.sentence = ""
        self.translatedLabel.setText(self.sentence + " " + self.currentWord)

    @Slot()
    def backspace(self):
        self.currentWord = self.currentWord[:-1]
        self.translatedLabel.setText(self.sentence + " " + self.currentWord)

    @Slot()
    def space(self):
        self.currentWord = ac.autoCorrect(self.currentWord)
        self.sentence += self.sentence + " " + self.currentWord
        self.translatedLabel.setText(self.sentence + " " + self.currentWord)


if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())
