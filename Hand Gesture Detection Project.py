import mediapipe as mp
import cv2
import pyautogui
import time
import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 1.0)

def speak(text):
    threading.Thread(target=_speak_thread, args=(text,)).start()

def _speak_thread(text):
    engine.say(text)
    engine.runAndWait()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)

last_gesture = None
gesture_cooldown = 1.0
last_action_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            tip_ids = [8, 12, 16, 20]
            fingers = [1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y else 0 for i in range(4)]

            finger_count = fingers.count(1)
            current_time = time.time()

            if finger_count == 0 and last_gesture != 'fist':
                print("Fist Detected - Play/Pause")
                speak("Play or Pause")
                pyautogui.press('space')
                last_gesture = 'fist'

            elif finger_count == 1 and last_gesture != 'index_finger' and current_time - last_action_time > gesture_cooldown:
                print("One Finger - Fast Forward")
                speak("Fast Forward")
                pyautogui.press('right')
                last_gesture = 'index_finger'
                last_action_time = current_time

            elif finger_count == 2 and last_gesture != 'two_finger' and current_time - last_action_time > gesture_cooldown:
                print("Two Fingers - Rewind")
                speak("Rewind")
                pyautogui.press('left')
                last_gesture = 'two_finger'
                last_action_time = current_time

            elif finger_count == 4 and last_gesture != 'open_palm' and current_time - last_action_time > gesture_cooldown:
                print("Open Palm Detected")
                speak("Open Palm Detected")
                last_gesture = 'open_palm'
                last_action_time = current_time

            elif 1 <= finger_count < 4:
                last_gesture = None

    else:
        last_gesture = None

    cv2.putText(frame, "Press 'Q' to Quit", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow('Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
