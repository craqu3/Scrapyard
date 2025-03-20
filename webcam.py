import cv2
import mediapipe as mp
import pyfirmata2
import random

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# Inicializa a placa Arduino
try:
    print("Conectando com a placa Arduino...")
    board = pyfirmata2.Arduino(pyfirmata2.Arduino.AUTODETECT)
    ledPin = board.get_pin('d:10:p')
    ledPin2 = board.get_pin('d:11:p')
    ledPin.write(1.0)
    print("Conexão com a placa Arduino estabelecida.")
except Exception as e:
    print(f"Erro ao conectar com a placa Arduino: {e}")
    board = None


dedo = random.randint(1,11)
print(dedo)
def webcam():
    print("Connecting camera")            
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0, 
        min_detection_confidence=0.9, 
        min_tracking_confidence=0.9) as hands:

        while cap.isOpened():
            success, image = cap.read() 
            if not success:
                #print("Ignorando frame vazio da câmera.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            fingerCount = 0

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                    handLabel = results.multi_handedness[handIndex].classification[0].label
                    handLandmarks = []

                    for landmarks in hand_landmarks.landmark:
                        handLandmarks.append([landmarks.x, landmarks.y])

                    if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                        fingerCount += 1
                    elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                        fingerCount += 1

                    if handLandmarks[8][1] < handLandmarks[6][1]:       # Dedo indicador
                        fingerCount += 1
                    if handLandmarks[12][1] < handLandmarks[10][1]:     # Dedo do meio
                        fingerCount += 1
                    if handLandmarks[16][1] < handLandmarks[14][1]:     # Dedo anelar
                        fingerCount += 1
                    if handLandmarks[20][1] < handLandmarks[18][1]:     # Dedo mindinho
                        fingerCount += 1

                    
                    
                    if board != None:
                        if fingerCount == 7:
                            ledPin.write(0)
                            ledPin2.write(1)
            
                            
                        else:
                            ledPin2.write(0)
                            ledPin.write(1)

                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

            cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 10)

            ret, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')

    cap.release()
    if board != None:
        board.exit()
    cv2.destroyAllWindows()
