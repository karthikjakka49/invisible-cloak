import cv2
import numpy as np
import time

# Take color input
color = input("Enter cloak color (red/blue/green/yellow/white): ").lower()

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened")
    exit()

time.sleep(2)

# Capture background
for i in range(60):
    ret, background = cap.read()

if not ret:
    print("Could not capture background")
    cap.release()
    exit()

background = cv2.flip(background, 1)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Set color range
    if color == "blue":
        lower = np.array([100, 100, 50])
        upper = np.array([140, 255, 255])

    elif color == "green":
        lower = np.array([35, 80, 50])
        upper = np.array([85, 255, 255])

    elif color == "yellow":
        lower = np.array([20, 100, 100])
        upper = np.array([35, 255, 255])

    elif color == "red":
        lower1 = np.array([0, 100, 50])
        upper1 = np.array([10, 255, 255])

        lower2 = np.array([170, 100, 50])
        upper2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)

        mask = mask1 + mask2

    elif color == "white":
        lower = np.array([0, 0, 180])
        upper = np.array([180, 80, 255])

    else:
        print("Color not supported")
        break

    # Create mask for colors except red
    if color != "red":
        mask = cv2.inRange(hsv, lower, upper)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_DILATE,
        kernel
    )

    # Inverse mask
    inverse_mask = cv2.bitwise_not(mask)

    # Normal part of image
    normal = cv2.bitwise_and(
        frame,
        frame,
        mask=inverse_mask
    )

    # Background where cloak is detected
    cloak = cv2.bitwise_and(
        background,
        background,
        mask=mask
    )

    # Combine
    result = cv2.add(normal, cloak)

    cv2.imshow("Invisible Cloak", result)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()