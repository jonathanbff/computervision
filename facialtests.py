import cv2
import time
import mediapipe as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Inicialização
mpFace = mp.solutions.face_mesh
mpDraw = mp.solutions.drawing_utils
face_mesh = mpFace.FaceMesh()

cap = cv2.VideoCapture(0)

pTime = 0
verde_florescente = (51, 0, 204)

face_draw_spec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

while True:
    success, img = cap.read()
    if not success:
        print("Falha na leitura do vídeo.")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results_face = face_mesh.process(imgRGB)

    # Desenhar landmarks da face
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            mpDraw.draw_landmarks(img, face_landmarks, landmark_drawing_spec=face_draw_spec)

    # Cálculo de FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)

    # Mostrar imagem
    cv2.imshow("Image", img)

    # Tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if results_face.multi_face_landmarks:
            # Plotar gráfico 3D com landmarks da última face detectada
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            for landmark in face_landmarks.landmark:
                ax.scatter(landmark.x, landmark.y, landmark.z, c='r', marker='o')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.show()
        break

cap.release()
cv2.destroyAllWindows()
