import cv2
import time
import mediapipe as mp
import random

# Inicialização
mpPose = mp.solutions.pose
mpDraw = mp.solutions.drawing_utils
pose = mpPose.Pose()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

pTime = 0
verde_florescente = (51, 0, 204)

# Variáveis para rastrear o estado, as contagens e os níveis
contagem = 0
circle_center = None
circle_color = None
circle_velocity = [2, 2]  # Velocidade inicial da bolinha (x, y)
nivel = 4  # Nível inicial
pontos_para_proximo_nivel = 5  # Pontos necessários para avançar para o próximo nível
usar_mao_direita = True  # Iniciar com a mão direita
mover_bolinha = True  # Controlar se a bolinha se move ou não
invert_video = False # inversão de vídeo

# Função para desenhar uma bolinha
def draw_circle(img, center, radius, color):
    cv2.circle(img, center, radius, color, -1)

# Função para aumentar a dificuldade
def aumentar_dificuldade(velocidade):
    return [v * 1.2 for v in velocidade]  # Aumenta a velocidade em 20%

while True:
    success, img = cap.read()
    if not success:
        print("Falha na leitura do vídeo.")
        break

    if invert_video:
        img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(imgRGB)



    if results_pose.pose_landmarks:
        mpDraw.draw_landmarks(img, results_pose.pose_landmarks, mpPose.POSE_CONNECTIONS)

        landmarks = results_pose.pose_landmarks.landmark

        # Alternar entre a mão direita e a mão esquerda dependendo do nível
        if usar_mao_direita:
            mao = (int(landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x * img.shape[1]),
                int(landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y * img.shape[0]))
        else:
            mao = (int(landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].x * img.shape[1]),
                   int(landmarks[mpPose.PoseLandmark.LEFT_WRIST.value].y * img.shape[0]))

        # Inicializar a bolinha se necessário
        if circle_center is None:
            circle_center = (random.randint(50, img.shape[1] - 50), random.randint(50, img.shape[0] - 50))
            circle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            mover_bolinha = random.choice([True, False])  # Decidir aleatoriamente se a bolinha vai se mover

        # Desenhar a bolinha
        draw_circle(img, circle_center, 50, circle_color)

        # Mover a bolinha se necessário
        if mover_bolinha:
            circle_center = (circle_center[0] + circle_velocity[0], circle_center[1] + circle_velocity[1])
            circle_center = (int(circle_center[0]), int(circle_center[1]))

            # Verificar colisões com as bordas
            if circle_center[0] <= 0 or circle_center[0] >= img.shape[1]:
                circle_velocity[0] *= -1
            if circle_center[1] <= 0 or circle_center[1] >= img.shape[0]:
                circle_velocity[1] *= -1

        # Verificar se a mão está próxima à bolinha
        distance = ((mao[0] - circle_center[0]) ** 2 + (mao[1] - circle_center[1]) ** 2) ** 0.5
        if distance < 30:
            contagem += 1
            circle_center = None  # Resetar a bolinha
            if contagem % pontos_para_proximo_nivel == 0:
                nivel += 1
                circle_velocity = aumentar_dificuldade(circle_velocity)
                usar_mao_direita = not usar_mao_direita  # Alternar a mão

        cv2.putText(img, f"Contagem: {contagem}", (70, 150), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)
        cv2.putText(img, f"Nível: {nivel}", (70, 170), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)
        mao_usada = "Direita" if usar_mao_direita else "Esquerda"
        cv2.putText(img, f"Mão: {mao_usada}", (70, 190), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 1, verde_florescente, 1)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
