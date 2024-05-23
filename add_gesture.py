from database import session, Gesture, Landmark

def add_gesture(name, description, landmarks):
    gesture = Gesture(name=name, description=description)
    session.add(gesture)
    session.commit()
    
    for index, (x, y) in enumerate(landmarks):
        landmark = Landmark(gesture_id=gesture.id, index=index, x=x, y=y)
        session.add(landmark)
    
    session.commit()

# Пример добавления жеста "Палец вверх"
thumbs_up_landmarks = [
    (0.5, 0.2),
    (0.5, 0.1),
    (0.3, 0.3),
    (0.3, 0.5),
    (0.3, 0.7),
    (0.3, 0.9)
]

add_gesture("Thumbs Up", "A thumbs up gesture", thumbs_up_landmarks)


# Пример добавления жеста "ОК"
ok_landmarks = [
    (0.5, 0.2),
    (0.5, 0.1),
    (0.4, 0.3),
    (0.4, 0.5),
    (0.4, 0.7),
    (0.4, 0.9)
]

add_gesture("OK", "An OK gesture", ok_landmarks)
