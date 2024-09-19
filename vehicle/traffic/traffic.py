import cv2
import numpy as np
import os
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
 
# Define full paths to the necessary files
weights_path = "traffic/yolov3.weights"
config_path = "traffic/yolov3.cfg"
names_path = "traffic/coco.txt"

# Check if files exist
if not os.path.exists(config_path):
    raise FileNotFoundError(f"Config file not found: {config_path}")
if not os.path.exists(weights_path):
    raise FileNotFoundError(f"Weights file not found: {weights_path}")
if not os.path.exists(names_path):
    raise FileNotFoundError(f"Names file not found: {names_path}")

# Load YOLO
net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()
unconnected_out_layers = net.getUnconnectedOutLayers()

# Check if unconnected_out_layers is an integer array
if isinstance(unconnected_out_layers, np.ndarray):
    output_layers = [layer_names[i - 1] for i in unconnected_out_layers.flatten()]
else:
    output_layers = [layer_names[i[0] - 1] for i in unconnected_out_layers]

# Load class names
with open(names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Open the webcam for real-time video capture
cap = cv2.VideoCapture(0)

detected_classes = set()

while cap.isOpened():
    # Reading the video stream
    ret, frame = cap.read()
    if ret:
        height, width, channels = frame.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Information to show on the screen
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Non-max suppression to eliminate redundant overlapping boxes with lower confidences
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        current_detected_classes = set()
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
                current_detected_classes.add(label)

        # Announce detected objects
        new_classes = current_detected_classes - detected_classes
        if new_classes:
            for detected_class in new_classes:
                engine.say(f"{detected_class} detected")
                engine.runAndWait()
            detected_classes.update(new_classes)

        # Showing the output frame
        cv2.imshow("Traffic Sign Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
