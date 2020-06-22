import sys
import cv2
from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Thread(QThread):
	changePixmap = pyqtSignal(QImage)

	def run(self):
		cap = cv2.VideoCapture(0)
		while True:
			return_value, image_frame = cap.read()
			if return_value:
				# Run the face detector
				image_frame, result = self.face_recognizer_method(image_frame)

				# Update the status based on the result
				self.line_edit_method(result)

				# Execute the motor control action
				if result == True:
					self.servo_motor_object.unlockDoor()
				else:
					self.servo_motor_object.lockDoor()

				# https://stackoverflow.com/a/55468544/6622587 For display to Qt
				rgb_image = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
				height, width, channels = rgb_image.shape
				bytes_per_line = channels * width
				convertToQtFormat = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
				p = convertToQtFormat.scaled(self.width, self.height, Qt.KeepAspectRatio)
				self.changePixmap.emit(p)

	def configure(self, width, height):
		self.width = width
		self.height = height

	def setFaceRecognizerMethod(self, incoming_face_recognizer_method):
		self.face_recognizer_method = incoming_face_recognizer_method

	def setLineDisplayMethod(self, incoming_line_edit_method):
		self.line_edit_method = incoming_line_edit_method

	def setServoMotorObject(self, incoming_servo_motor_object):
		self.servo_motor_object = incoming_servo_motor_object

class QWidgetApplication(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 Video'
		self.left = 100
		self.top = 10
		self.width = 1400

		self.height = 1140
		self.margin = 10
		self.initUI()
		# self.info_text_box(self.printNothing)

	@pyqtSlot(QImage)
	def setImage(self, image):
		self.label.setPixmap(QPixmap.fromImage(image))

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

		self.setLayout(vbox)

		self.thread_object = Thread(self)
		self.thread_object.configure(self.width-self.margin*2, int((self.width-self.margin*2) /1.33))
		self.thread_object.changePixmap.connect(self.setImage)
		self.thread_object.setLineDisplayMethod(self.displayUpdates)
		self.thread_object.start()
		self.show()

	def displayUpdates(self, input_status):
		if input_status == True:
			self.info_text_box.setText("Face ID Found, Unlocking Door!")
		else:
			self.info_text_box.setText("No face ID found")

	def attachFaceRecognizerObject(self, incoming_face_recognizer_object):
		self.face_recognizer_object = incoming_face_recognizer_object
		self.thread_object.setFaceRecognizerMethod(self.face_recognizer_object.runFaceRecognizer)

	def attachServoMotorObject(self, incoming_servo_motor_object):
		self.servo_motor_object = incoming_servo_motor_object
		self.thread_object.setServoMotorObject(self.servo_motor_object)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = QWidgetApplication()
	sys.exit(app.exec_())