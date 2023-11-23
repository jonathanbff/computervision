import mediapipe as mp
import cv2

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Define a function to check for the "OK" gesture
def is_ok_gesture(hand_landmarks, frame):
    # Get the tip of the thumb and index finger
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Calculate the distance between the thumb tip and index tip
    distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5

    # Check if the distance is small enough to consider the gesture as "OK"
    # You may need to adjust the threshold based on the scale of the coordinates
    if distance < 0.05:
        # Draw or annotate the gesture on the frame
        cv2.putText(frame, 'OK', (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image and draw hand landmarks
    result = hands.process(image_rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Annotate landmarks
            for idx, landmark in enumerate(hand_landmarks.landmark):
                # Get coordinates
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])

                # Draw text
                cv2.putText(frame, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Check for the "OK" gesture
            is_ok_gesture(hand_landmarks, frame)

    # Display the frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
