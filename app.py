# Written by Xavier Koh and Jerald Tee

# Import Dependencies
import sys
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QImage,  QPixmap
from PySide6.QtWidgets import (QApplication,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget, QCheckBox)
import autocorrect as ac
import detection as dt
import time
import cv2


# Declare video output thread
class ImageThread(QThread):
    updateFrame = Signal(QImage)
    
    # Initialise Thread
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

        # Declare variables
        self.status = True

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.status:
            # Run function from detection.py and save cv2 img data
            frame = dt.detectImg(self.cap.read(0))[0]

            # Convert image color type
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert image into QImage and scale image to 960x540 pixels
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
            scaled_img = img.scaled(960, 540, Qt.KeepAspectRatio)

            # Emit output image
            self.updateFrame.emit(scaled_img)
        sys.exit(-1)


# Declare gesture check thread
class UpdateThread(QThread):
    updateLabel = Signal(str)

    # Initialise Thread
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)

        # Declare variables
        self.prevChar = 'nothing'
        self.prevchangetime = time.time()


    def run(self):
        self.cap = cv2.VideoCapture(0)
        while True:
            # Save current program time
            self.currenttime = time.time()

            # Run function from detection.py and save the detected class
            self.predicted_char = dt.detectImg(self.cap.read())[1]

            # Code below detects when a class has been detected for > 1 second and saves it
            # Check if the detected class has changed and reset the previous change time
            if self.predicted_char != self.prevChar:
                self.prevchangetime = time.time()
                self.prevChar = self.predicted_char
            
            # Checks if time between current program time and the time when the detected class was last change is > 1 sec
            if self.currenttime - self.prevchangetime >= 1 and self.predicted_char != 'nothing' and self.predicted_char != 'del':

                # Reset previous class change time to allow for multiple subsequent detections of the same class
                self.prevchangetime = time.time()

                # Emit detected class
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
        self.autocorrectEnabled = False

        # Thread in charge of updating the image
        self.ith = ImageThread(self)
        self.ith.updateFrame.connect(self.setImage)

        # Thread in charge of when to update the translated text label
        self.uth = UpdateThread(self)
        self.uth.updateLabel.connect(self.updateText)

        # Translation label layout
        self.translatedLabel = QLabel()
        self.translatedLabel.setWordWrap(True)

        # Bottom Row layout
        buttons_layout = QHBoxLayout()
        self.spaceButton = QPushButton("Next Word")
        self.backspaceButton = QPushButton("Backspace")
        self.resetButton = QPushButton("Reset")
        self.acCheckbox = QCheckBox("Enable Autocorrect")
        self.spaceButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.backspaceButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.resetButton.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.spaceButton)
        buttons_layout.addWidget(self.backspaceButton)
        buttons_layout.addWidget(self.resetButton)
        buttons_layout.addWidget(self.acCheckbox)

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
        self.acCheckbox.toggled.connect(self.checkboxCheck)
        self.resetButton.clicked.connect(self.reset)
        self.backspaceButton.clicked.connect(self.backspace)
        self.spaceButton.clicked.connect(self.space)

    @Slot()
    def start(self):
        print("Starting...")
        # Starts both threads
        self.ith.start()
        self.uth.start()

    @Slot()
    def checkboxCheck(self):

        # Checks if autocorrect checkbox is ticked and updates variable
        if self.acCheckbox.isChecked(): 
            self.autocorrectEnabled = True
            print('autocorrect enabled')
        else:
            self.autocorrectEnabled = False
            print("autocorrect disabled")

    @Slot(QImage)
    def setImage(self, image):
        # Updates currently displayed frame when new frame is available
        self.displayLabel.setPixmap(QPixmap.fromImage(image))

    @Slot(str)
    def updateText(self, nextchar):
        # Adds new character to current word when character has been held for > 1 second
        self.currentWord += nextchar
        self.translatedLabel.setText(self.sentence + " " + self.currentWord)

    @Slot()
    def reset(self):
        # Resets translated text label
        self.sentence = ""
        self.currentWord = ""
        self.translatedLabel.setText(self.sentence + " " + self.currentWord)

    @Slot()
    def backspace(self):
        # Removes last index from current word string
        self.currentWord = self.currentWord[:-1]
        self.translatedLabel.setText(self.sentence + " " + self.currentWord)

    @Slot()
    def space(self):
        # Checks if autocorrect is enabled
        if self.autocorrectEnabled == True:
            # Runs autocorrect and appends autocorrected word to the sentence
            self.currentWord = ac.autoCorrect(self.currentWord).upper()
            self.sentence += " " + self.currentWord
            self.currentWord = ""
            self.translatedLabel.setText(self.sentence)
        else:
            # Append current word to the sentence
            self.sentence += " " + self.currentWord
            self.currentWord = ""
            self.translatedLabel.setText(self.sentence)

# Runs app
if __name__ == "__main__":
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())