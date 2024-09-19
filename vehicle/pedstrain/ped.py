import cv2
import imutils
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties for the voice (optional)
engine.setProperty('rate', 150)    # Speed of speech
engine.setProperty('volume', 1)    # Volume (0.0 to 1.0)

# Initialize the HOG person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Open the webcam for real-time video capture
cap = cv2.VideoCapture(0)

# Variables to store previous regions
prev_regions = []

while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()
    if ret:
        image = imutils.resize(image, width=min(900, image.shape[1]))

        # Detecting all the regions in the image that have a pedestrian inside them
        (regions, _) = hog.detectMultiScale(image, winStride=(4, 4), padding=(4, 4), scale=1.05)

        # Drawing the regions in the image and handling detections
        for (x, y, w, h) in regions:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Check if a person is crossing
        crossing_detected = False
        for (px, py, pw, ph) in prev_regions:
            for (x, y, w, h) in regions:
                if abs(px - x) > 50 and abs(py - y) < 50:
                    crossing_detected = True
                    break
            if crossing_detected:
                break

        # Text-to-speech alert
        if crossing_detected:
            engine.say("A person is crossing the road")
            engine.runAndWait()  # Wait for the speech to finish

        # Update previous regions
        prev_regions = regions

        # Showing the output image
        cv2.imshow("Image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
