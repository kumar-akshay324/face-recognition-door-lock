import sys
import cv2
# from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
# from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Thread(QThread):
	changePixmap = pyqtSignal(QImage)

	def run(self):
		cap = cv2.VideoCapture(0)
		while True:
			ret, image_frame = cap.read()
			if ret:
				# https://stackoverflow.com/a/55468544/6622587
				image_frame, creds = self.face_recognizer_method(image_frame)
				rgbImage = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
				h, w, ch = rgbImage.shape
				bytesPerLine = ch * w
				convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
				p = convertToQtFormat.scaled(self.width, self.height, Qt.KeepAspectRatio)
				self.changePixmap.emit(p)

	def configure(self, width, height):
		self.width = width
		self.height = height

	def setFaceRecognizerMethod(self, incoming_face_recognizer_method):
		self.face_recognizer_method = incoming_face_recognizer_method

class QWidgetApplication(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 Video'
		self.left = 100
		self.top = 10
		self.width = 1024

		self.height = 840
		self.margin = 10
		self.initUI()
		self.connectAddNewFaceButton(self.printNothing)

	@pyqtSlot(QImage)
	def setImage(self, image):
		self.label.setPixmap(QPixmap.fromImage(image))

	def printNothing(self):
		print ("Clicked")

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		self.label = QLabel(self)
		self.label.move(self.margin, self.margin)
		self.label.resize(self.width-self.margin*2, int((self.width-self.margin*2) /1.33))

		vbox = QVBoxLayout()
		vbox.addStretch()

		self.info_text_box = QLineEdit()
		self.info_text_box.setReadOnly(True)
		self.info_text_box.setText("Nothing here")
		self.info_text_box.setAlignment(Qt.AlignCenter)

		vbox.addStretch()
		vbox.addWidget(self.info_text_box)

		hbox = QHBoxLayout()

		self.add_new_face_button = QPushButton("Add New Face")
		hbox.addWidget(self.add_new_face_button)
		self.unlock_button = QPushButton("Unlock")
		hbox.addWidget(self.unlock_button)

		vbox.addLayout(hbox)

		self.setLayout(vbox)

		self.thread_object = Thread(self)
		self.thread_object.configure(self.width-self.margin*2, int((self.width-self.margin*2) /1.33))
		self.thread_object.changePixmap.connect(self.setImage)
		self.thread_object.start()
		self.show()

	def displayUpdates(self, input_text):
		self.info_text_box.setText(input_text)

	def printClicked(self):
		print ("Button Clicked")

	def connectAddNewFaceButton(self, incoming_object_function):
		self.add_new_face_button.clicked.connect(incoming_object_function)

	def attachFaceRecognizerObject(self, incoming_face_recognizer_object):
		self.face_recognizer_object = incoming_face_recognizer_object
		self.thread_object.setFaceRecognizerMethod(self.face_recognizer_object.runFaceRecognizer)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = QWidgetApplication()
	sys.exit(app.exec_())