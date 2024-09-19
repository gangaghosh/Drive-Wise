import cv2
import numpy as np

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines):
    if lines is None:
        return img
    img = np.copy(img)
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    left_lines = []
    right_lines = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            if x2 - x1 == 0:  # avoid divide by zero
                continue
            slope = (y2 - y1) / (x2 - x1)
            if slope < 0:
                left_lines.append((x1, y1, x2, y2))
            else:
                right_lines.append((x1, y1, x2, y2))

    left_lane = average_slope_intercept(img, left_lines)
    right_lane = average_slope_intercept(img, right_lines)

    if left_lane is not None:
        draw_line(blank_image, left_lane)
    if right_lane is not None:
        draw_line(blank_image, right_lane)

    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

def draw_line(img, line):
    x1, y1, x2, y2 = line
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), thickness=5)

def average_slope_intercept(img, lines):
    if len(lines) == 0:
        return None
    x_coords = []
    y_coords = []
    for x1, y1, x2, y2 in lines:
        x_coords.extend([x1, x2])
        y_coords.extend([y1, y2])
    if len(x_coords) == 0:
        return None
    poly = np.polyfit(x_coords, y_coords, 1)
    slope = poly[0]
    intercept = poly[1]
    y1 = img.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return (x1, y1, x2, y2)

def process(image):
    height, width = image.shape[:2]
    region_of_interest_vertices = [
        (0, height),
        (width / 2, height / 2),
        (width, height)
    ]

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny_image = cv2.Canny(blur_image, 50, 150)
    cropped_image = region_of_interest(
        canny_image,
        np.array([region_of_interest_vertices], np.int32)
    )

    lines = cv2.HoughLinesP(
        cropped_image,
        rho=2,
        theta=np.pi / 180,
        threshold=50,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=100
    )

    image_with_lines = draw_lines(image, lines)
    return image_with_lines

def main():
    cap = cv2.VideoCapture(0)  # Use the webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        frame = process(frame)
        cv2.imshow('Lane Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
