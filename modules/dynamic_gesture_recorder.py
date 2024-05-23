import cv2
import mediapipe as mp
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import QTimer, QDateTime
from PyQt6.QtGui import QImage, QPixmap
from database import session, Gesture, GestureFrame, Landmark

class DynamicGestureRecorder(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Input field for gesture name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter gesture name")
        self.layout.addWidget(self.name_input)

        # Button to start/stop recording gesture
        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        self.layout.addWidget(self.record_button)

        # Label to show camera feed
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)
        
        self.setLayout(self.layout)
        
        # Initialize Hand Tracking module from MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        # Initialize OpenCV video capture
        self.cap = cv2.VideoCapture(0)

        # Initialize QTimer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.recording = False
        self.frames = []
        self.current_gesture = None

    def toggle_recording(self):
        if self.recording:
            self.record_button.setText("Start Recording")
            self.recording = False
            self.save_gesture()
        else:
            gesture_name = self.name_input.text()
            if not gesture_name:
                print("Please enter a gesture name")
                return

            self.record_button.setText("Stop Recording")
            self.recording = True
            self.frames = []
            self.current_gesture = Gesture(name=gesture_name)
            session.add(self.current_gesture)
            session.commit()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip the camera frame horizontally
        frame_flipped = cv2.flip(frame, 1)

        # Convert the flipped frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)

        # Process the frame with Hand Tracking
        results = self.hands.process(rgb_frame)

        # Draw landmarks on the hands
        if results.multi_hand_landmarks:
            # Initialize drawing utilities outside the loop
            mp_drawing = mp.solutions.drawing_utils
            
            frame_landmarks = []
            for hand_landmarks in results.multi_hand_landmarks:
                for point in hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    x, y = int(point.x * w), int(point.y * h)
                    cv2.circle(frame_flipped, (x, y), 5, (255, 0, 0), -1)
                    frame_landmarks.append((point.x, point.y, point.z))

                # Draw hand connections
                mp_drawing.draw_landmarks(frame_flipped, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            if self.recording:
                self.frames.append(frame_landmarks)

        # Convert frame to QImage
        height, width, channel = frame_flipped.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame_flipped.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)

        # Set QImage to QLabel
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def save_gesture(self):
        if not self.frames or not self.current_gesture:
            return

        for frame_number, landmarks in enumerate(self.frames):
            gesture_frame = GestureFrame(
                gesture_id=self.current_gesture.id,
                frame_number=frame_number,
                timestamp=frame_number * 30 / 1000.0  # Example: assuming 30ms per frame
            )
            session.add(gesture_frame)
            session.commit()

            for index, (x, y, z) in enumerate(landmarks):
                landmark = Landmark(
                    gesture_frame_id=gesture_frame.id,
                    index=index,
                    x=x,
                    y=y,
                    z=z
                )
                session.add(landmark)

        session.commit()
        print(f"Dynamic gesture '{self.current_gesture.name}' saved successfully!")
        self.current_gesture = None

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    window = DynamicGestureRecorder()
    window.show()
    app.exec()
