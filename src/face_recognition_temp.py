import face_recognition
import cv2, os, sys
import numpy as np
from gui_app import QWidgetApplication

from PyQt5.QtGui import QImage, QPixmap

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class FaceRecognizer:
    def __init__(self):
        self.frame_count, self.jump_frames = 0, 3
        self.known_face_encodings = []
        self.known_face_names = []
        self.initializeKnownFaces()

    def initializeKnownFaces(self):
        folder_abs = os.getcwd() + os.path.sep + "saved_images"
        print ("Making Encodings for folder: {}".format(folder_abs))
        for image_file in os.listdir(folder_abs):
            face_identity = image_file.split(".")[0]
            print ("\nFor file: {}".format(image_file))

            image_file_abs = folder_abs + os.path.sep + image_file
            image = face_recognition.load_image_file(image_file_abs)

            face_encoding = face_recognition.face_encodings(image)[0]
            print ("Encodings Generated")

            # Create arrays of known face encodings and their names
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(face_identity)

    def learnNewFace(self, new_image, new_image_name):
        print ("\nGenerating New Encoding for: {}".format(new_image_name))

        face_encoding = face_recognition.face_encodings(new_image)[0]
        print ("Encodings Generated And Added To Known Images")

        # Create arrays of known face encodings and their names
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(new_image_name)

    def runFaceRecognizer(self, incoming_image_frame):
        credentials_confirmed = False
        # Resizing to 1/3rd of the image for quick face recognition algorithm execution
        scaled_image = cv2.resize(incoming_image_frame, (0, 0), fx = 1/3, fy = 1/3)

        # Convert the image from OpenCV BGR to RGB color for the  face_recognition library
        scaled_image = scaled_image[:, :, ::-1]

        # Only the Nth frame will be processed to be more computationally efficient
        if self.frame_count % self.jump_frames != 0:
            return
        else:
            self.frame_count = 0

        # Find all the faces and face encodings in the current frame of video
        self.current_face_locations = face_recognition.face_locations(scaled_image)
        current_face_encodings = face_recognition.face_encodings(scaled_image, self.current_face_locations)

        self.recognized_face_names = []
        for current_face_encoding in current_face_encodings:
            # Fetch matches between the current face against the known face encodings
            face_matches = face_recognition.compare_faces(self.known_face_encodings, current_face_encoding)
            name = "Unknown"

            # Define the best match as the image with the smallest distance difference
            current_face_distances = face_recognition.face_distance(self.known_face_encodings, current_face_encoding)
            best_match_idx = np.argmin(current_face_distances)
            if face_matches[best_match_idx]:
                name = self.known_face_names[best_match_idx]

            self.recognized_face_names.append(name)
            if name == "Unknown":
                credentials_confirmed = True

        self.displayNamesInImage(incoming_image_frame)
        return incoming_image_frame, credentials_confirmed

    def displayNamesInImage(self, incoming_image_frame):
        # Display the various bounding boxes and corresponding names in the Display
        for (top_loc, right_loc, bottom_loc, left_loc), recognized_face_name in zip(self.current_face_locations, self.recognized_face_names):
            # Upscaling for each feature by the scaling factor since this will be displayed in the original image
            top_loc *= 3
            right_loc *= 3
            bottom_loc *= 3
            left_loc *= 3

            # Box around the face
            cv2.rectangle(incoming_image_frame, (left_loc, top_loc), (right_loc, bottom_loc), (0, 0, 255), 2)

            # Write the name label for the image
            cv2.rectangle(incoming_image_frame, (left_loc, bottom_loc - 50), (right_loc, bottom_loc), (0, 0, 255), cv2.FILLED)
            cv2.putText(incoming_image_frame, recognized_face_name, (left_loc + 6, bottom_loc - 6), cv2.FONT_ITALIC, 1.0, (255, 255, 255), 1)

if __name__ == "__main__":
    qt_app = QApplication(sys.argv)

    face_recognizer_object = FaceRecognizer()
    gui_app_object = QWidgetApplication()
    gui_app_object.attachFaceRecognizerObject(face_recognizer_object)
    sys.exit(qt_app.exec_())
