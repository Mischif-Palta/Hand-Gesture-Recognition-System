Gesture-Controlled Video Playback Using Python

Overview
This project introduces a gesture-controlled interface for media playback, combining computer vision and Python. By integrating OpenCV, Mediapipe, and PyAutoGUI, it detects 
real-time hand gestures and maps them to media control actions, making interactions more intuitive and accessible.

Features
Real-time Hand Gesture Recognition
Gesture-Based Media Playback Controls
Seamless Integration with Video Players
Visual Feedback via OpenCV Interface

Gesture Controls
Fist (✊) → Play/Pause the video
One Finger Up (☝️) → Fast-forward
Two Fingers Up (✌️) → Rewind
Open Palm (🖐️) → Detect Open Hand State

How It Works
Hand Tracking: Mediapipe detects and tracks hand landmarks in real-time.
Gesture Recognition: The system analyzes finger positions to classify gestures.
Action Execution: PyAutoGUI sends the appropriate keystrokes to control media playback.

Technology Stack
Programming Language: Python
Libraries: OpenCV, Mediapipe, PyAutoGUI

Contributions are encouraged. Feel free to fork the repository, submit pull requests, or share suggestions for improvement.
