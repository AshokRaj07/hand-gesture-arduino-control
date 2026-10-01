import cv2
import mediapipe as mp
import serial
import time

# Initialize mediapipe hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)
ser = serial.Serial('COM3', 9600,timeout=1)
time.sleep(2)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Camera not found or not accessible.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (MediaPipe needs RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    # If hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

            # Define finger tips (fingertip landmarks: 8, 12, 16, 20)
            tips = [8, 12, 16, 20]
            # Determine if the fingers are open or closed by comparing y-coordinates
            fingers = [hand_landmark.landmark[tip].y < hand_landmark.landmark[tip - 2].y for tip in tips]

            # Check if all fingers are open (tips are above the knuckles)
            if all(fingers):
                print("Opened")
                ser.write(b'1')
            # Check if none of the fingers are open (all tips are below knuckles)
            elif not any(fingers):
                print("Not opened")
                ser.write(b'0')
            
            

    # Display the frame with the hand landmarks
    cv2.imshow("Hand Detection", frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
ser.close()
cv2.destroyAllWindows()
