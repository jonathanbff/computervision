import cv2
import time
import mediapipe as mp

# Inicialização
mpPose = mp.solutions.pose
mpFace = mp.solutions.face_mesh
mpDraw = mp.solutions.drawing_utils
pose = mpPose.Pose()
face_mesh = mpFace.FaceMesh()

#caso em que o vídeo está na pasta
#cap = cv2.VideoCapture('Treino 1 - Teo.mp4')


#realtime caso

cap = cv2.VideoCapture(0)

pTime = 0

verde_florescente = (51, 0, 204)

# Variáveis para rastrear o estado e as contagens
estado_anterior = ""
contagem = 0
ombro_anterior = None

# Especificações para desenho dos marcos faciais
face_draw_spec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

while True:
    success, img = cap.read()
    if not success:
        print("Falha na leitura do vídeo.")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(imgRGB)
    results_face = face_mesh.process(imgRGB)

    if results_pose.pose_landmarks:
        mpDraw.draw_landmarks(img, results_pose.pose_landmarks, mpPose.POSE_CONNECTIONS)

        landmarks = results_pose.pose_landmarks.landmark
        ombro_atual = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value].y
        quadril = landmarks[mpPose.PoseLandmark.LEFT_HIP.value].y
        joelho = landmarks[mpPose.PoseLandmark.LEFT_KNEE.value].y

        estado_atual = "levantado" if joelho > quadril else "sentado"

        if estado_atual != estado_anterior:
            contagem += 1
            estado_anterior = estado_atual

        if ombro_anterior:
            if ombro_atual > ombro_anterior:
                movimento_ombro = "subindo"
            elif ombro_atual < ombro_anterior:
                movimento_ombro = "descendo"
            else:
                movimento_ombro = "estável"
            cv2.putText(img, f"Ombro: {movimento_ombro}", (70, 200), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)

        ombro_anterior = ombro_atual

        cv2.putText(img, f"Estado: {estado_atual}", (70, 100), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)
        cv2.putText(img, f"Contagem: {contagem // 2}", (70, 150), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)

    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            mpDraw.draw_landmarks(img, face_landmarks, landmark_drawing_spec=face_draw_spec)

            upper_lip = face_landmarks.landmark[61].y
            lower_lip = face_landmarks.landmark[291].y

            if lower_lip > upper_lip:
                facial_expression = "Sorrindo"
            else:
                facial_expression = "Neutro"

            cv2.putText(img, f"Expressão: {facial_expression}", (70, 250), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente,
                        1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()