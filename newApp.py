from ctypes import alignment
from re import A
import sys
from textwrap import wrap
from tkinter import W
from turtle import right
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
import tensorflow as tf
import numpy as np

from cv2 import QRCodeDetector
from matplotlib.widgets import Widget
import os
import time

import cv2

model_path = 'model/asl_model'
predicted_char = "nothing"
model_path = 'model/asl_model'


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
        self.cap = True

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
            scaled_img = img.scaled(960, 540, Qt.KeepAspectRatio)

            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Title and dimensions
        self.setWindowTitle("ASL Recognition")
        self.setGeometry(0, 0, 800, 500)

        # Create a label for the display camera
        self.displayLabel = QLabel(self)
        self.displayLabel.setFixedSize(960, 540)

        # Thread in charge of updating the image
        self.th = Thread(self)
        self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        # Labels layout
        self.translatedLabel = QLabel("Translated text goes here")
        self.translatedLabel.setWordWrap(True)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.startButton = QPushButton("Start")
        self.stopButton = QPushButton("Stop/Close")
        self.startButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.stopButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.stopButton)
        buttons_layout.addWidget(self.startButton)

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
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.kill_thread)
        self.stopButton.setEnabled(False)

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.th.cap.release()
        cv2.destroyAllWindows()
        self.status = False
        self.th.terminate()
        # Give time for the thread to finish
        time.sleep(1)

    @Slot()
    def start(self):
        print("Starting...")
        self.stopButton.setEnabled(True)
        self.startButton.setEnabled(False)
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.displayLabel.setPixmap(QPixmap.fromImage(image))


if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    print("rendered")
    sys.exit(app.exec())