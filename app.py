import sys
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QImage,  QPixmap
from PySide6.QtWidgets import (QApplication,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
import autocorrect as ac
import detection as dt
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

            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(960, 540, Qt.KeepAspectRatio)

            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


class UpdateThread(QThread):
    updateLabel = Signal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
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
            if self.currenttime - self.prevchangetime >= 0.5 and self.predicted_char != 'nothing' and self.predicted_char != 'delete':
                self.prevchangetime = time.time()
                self.updateLabel.emit(self.predicted_char)


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
        self.autocorrectEnabled = True

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

    @Slot(str)
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
        self.translatedLabel.setText(self.sentence)


if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())
