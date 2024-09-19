from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import pyttsx3
import argparse
import imutils
import time
import dlib
import cv2

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0, help="index of webcam on system")
args = vars(ap.parse_args())

# Try different backends
# Example with CAP_DSHOW backend
vs = cv2.VideoCapture(args["webcam"], cv2.CAP_DSHOW)

# Example with CAP_FFMPEG backend
# vs = cv2.VideoCapture(args["webcam"], cv2.CAP_FFMPEG)

# Load facial landmark predictor
predictor_path = r"driver-fatigue-detection-system-master/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

# Function to compute the eye aspect ratio (EAR)
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Define constants for EAR threshold and consecutive frames
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 48

# Initialize the frame counter and alarm status
COUNTER = 0
ALARM_ON = False

# Initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector()

# Grab the indexes of the facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

# Loop over frames from the video stream
while True:
    # Grab the frame from the threaded video file stream
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Loop over the face detections
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                if not ALARM_ON:
                    ALARM_ON = True
                    engine.say("Drowsiness detected! Please wake up !")
                    engine.runAndWait()
        else:
            COUNTER = 0
            ALARM_ON = False

        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# Do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()


