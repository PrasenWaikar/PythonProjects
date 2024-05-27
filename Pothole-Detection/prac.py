import cv2
import numpy as np

# Read the image
image = cv2.imread("D:\VS code\Pothole-Detection-main\pothole1.jpg")
image = cv2.imread("D:\VS code\Pothole-Detection-main\pothole2.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to smooth the image
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blur, 50, 150)

# Find contours in the edges
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 100:  # Adjust this value based on your image
        cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)

# Display the result
cv2.imshow("Pothole Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
