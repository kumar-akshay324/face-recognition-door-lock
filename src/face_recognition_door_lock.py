from motor_contro.servo_control import ServoMotor

class FaceRecognitionDoorLock:
	def __init__(self):
		self.servo_motor = ServoMotor()
		self.face_recognizer = self.initializeFaceRecognitionEngine() 

	def initializeFaceRecognitionEngine():




