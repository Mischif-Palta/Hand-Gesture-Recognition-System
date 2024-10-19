import mediapipe as mp
import cv2
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

cap = cv2.VideoCapture(0)

last_gesture = None  

while cap.isOpened():
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            tip_ids = [4, 8, 12, 16, 20]
            fingers = []

            if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
                fingers.append(1)
            else:
                fingers.append(0)

            for finger_index in range(1, 5):
                if hand_landmarks.landmark[tip_ids[finger_index]].y < hand_landmarks.landmark[tip_ids[finger_index] - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            finger_count = fingers.count(1)  

            # Gesture detection logic
            if finger_count == 0 and last_gesture != 'fist':
                print("Fist Detected - Pausing/Playing video")  
                cv2.putText(frame, 'Fist Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), 2)  # Display message
                pyautogui.press('space')  
                last_gesture = 'fist'
            elif finger_count == 1 and last_gesture != 'index_finger':
                print("One Finger Detected - Next")
                cv2.putText(frame, "One Finger Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), 2)
                pyautogui.press('right')
                last_gesture = 'index_finger'
            elif finger_count == 2 and last_gesture != 'two_finger':
                print("Two Fingers Detected - Next")
                cv2.putText(frame, "Two Fingers Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), 2)
                pyautogui.press('left')
                last_gesture = 'two_finger'
            elif finger_count == 5 and last_gesture != 'open_palm':
                print("Open Palm Detected") 
                cv2.putText(frame, 'Open Palm Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), 2)  
                last_gesture = 'open_palm'  
            elif finger_count > 0 and finger_count < 5:
                last_gesture = None  

    else:
        last_gesture = None  

    cv2.imshow('Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()