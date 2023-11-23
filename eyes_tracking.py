import cv2
import mediapipe as mp
import numpy as np

# Inicialização
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Realtime caso
cap = cv2.VideoCapture(0)

# Iris landmarks
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

while True:
    success, img = cap.read()
    if not success:
        print("Falha na leitura do vídeo.")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(imgRGB)
    ih, iw, ic = img.shape

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw the face mesh
            mp_drawing.draw_landmarks(img, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION, drawing_spec, drawing_spec)

            # Calculate the center of the left iris
            left_iris_points = [face_landmarks.landmark[p] for p in LEFT_IRIS]
            left_iris_center = np.mean([(point.x * iw, point.y * ih) for point in left_iris_points], axis=0)

            # Calculate the center of the right iris
            right_iris_points = [face_landmarks.landmark[p] for p in RIGHT_IRIS]
            right_iris_center = np.mean([(point.x * iw, point.y * ih) for point in right_iris_points], axis=0)

            # Draw translucent circles at the iris centers
            overlay = img.copy()
            cv2.circle(overlay, tuple(np.round(left_iris_center).astype(int)), 20, (0, 0, 255, 0.6), -1)  # Semi-transparent red circle
            cv2.circle(overlay, tuple(np.round(right_iris_center).astype(int)), 20, (0, 0, 255, 0.6), -1)  # Semi-transparent red circle
            alpha = 0.4  # Transparency factor
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
