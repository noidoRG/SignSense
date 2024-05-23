import cv2
import mediapipe as mp
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from database import session, Gesture, Landmark

class GestureRecorder(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Input field for gesture name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter gesture name")
        self.layout.addWidget(self.name_input)

        # Button to save gesture
        self.save_button = QPushButton("Save Gesture")
        self.save_button.clicked.connect(self.save_gesture)
        self.layout.addWidget(self.save_button)

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

        self.current_landmarks = []

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

        self.current_landmarks = []

        # Draw landmarks on the hands
        if results.multi_hand_landmarks:
            # Initialize drawing utilities outside the loop
            mp_drawing = mp.solutions.drawing_utils
            
            for hand_landmarks in results.multi_hand_landmarks:
                for point in hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    x, y = int(point.x * w), int(point.y * h)
                    cv2.circle(frame_flipped, (x, y), 5, (255, 0, 0), -1)
                    self.current_landmarks.append((point.x, point.y))

                # Draw hand connections
                mp_drawing.draw_landmarks(frame_flipped, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # Convert frame to QImage
        height, width, channel = frame_flipped.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame_flipped.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)

        # Set QImage to QLabel
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def save_gesture(self):
        gesture_name = self.name_input.text()
        if not gesture_name or len(self.current_landmarks) < 21:
            print("Invalid gesture data")
            return
        
        # Create new gesture entry
        new_gesture = Gesture(name=gesture_name)
        session.add(new_gesture)
        session.commit()

        # Add landmarks to database
        for i, (x, y) in enumerate(self.current_landmarks):
            new_landmark = Landmark(gesture_id=new_gesture.id, index=i, x=x, y=y)
            session.add(new_landmark)

        session.commit()
        print(f"Gesture '{gesture_name}' saved successfully!")

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    window = GestureRecorder()
    window.show()
    app.exec()
