import cv2
import mediapipe as mp
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

class AnalyzerModule(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.layout = QVBoxLayout()
        self.image_label = QLabel()
        self.score_label = QLabel("Thumbs up: 0%")
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.score_label)
        self.setLayout(self.layout)
        
        # Initialize Hand Tracking module from MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        # Define the reference landmarks for a "thumbs up" gesture
        self.thumbs_up_reference = [
            (0.5, 0.2),  # Base of the thumb
            (0.5, 0.1),  # Tip of the thumb
            (0.3, 0.3),  # Tip of the index finger
            (0.3, 0.5),  # Tip of the middle finger
            (0.3, 0.7),  # Tip of the ring finger
            (0.3, 0.9),  # Tip of the pinky finger
        ]

        # Initialize OpenCV video capture
        self.cap = cv2.VideoCapture(0)

        # Initialize QTimer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

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

        # Initialize resemblance score
        resemblance_score = 0

        # Draw landmarks on the hands
        if results.multi_hand_landmarks:
            # Initialize drawing utilities outside the loop
            mp_drawing = mp.solutions.drawing_utils
            
            for hand_landmarks in results.multi_hand_landmarks:
                for point in hand_landmarks.landmark:
                    h, w, _ = frame.shape
                    x, y = int(point.x * w), int(point.y * h)
                    cv2.circle(frame_flipped, (x, y), 5, (255, 0, 0), -1)

                # Calculate resemblance score
                thumb_up_points = [(hand_landmarks.landmark[i].x, hand_landmarks.landmark[i].y)
                    for i in [2, 4, 8, 12, 16, 20]]  # Thumb, Index, Middle, Ring, Pinky fingers
                # Calculate dissimilarity score
                dissimilarity_score = sum(np.linalg.norm(np.array(thumb_up_points[i]) - np.array(self.thumbs_up_reference[i]))
                    for i in range(len(thumb_up_points))) / len(thumb_up_points)

                # Calculate resemblance score
                resemblance_score = 1 - dissimilarity_score

                # Draw hand connections
                mp_drawing.draw_landmarks(frame_flipped, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # Display the resemblance score
        self.score_label.setText(f'Thumbs up: {int(resemblance_score * 100)}%')

        # Convert frame to QImage
        height, width, channel = frame_flipped.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame_flipped.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)

        # Set QImage to QLabel
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)
