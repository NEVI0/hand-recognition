import cv2
import mediapipe as mp


class HandDetector:
    results: any

    def __init__(self, mode=False, max_hands=2, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(mode, max_hands, detection_con, track_con)

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_ldm in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_ldm, self.mp_hands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_number=0):
        landmark_list = []

        if self.results.multi_hand_landmarks:
            current_hand = self.results.multi_hand_landmarks[hand_number]

            for index, lm in enumerate(current_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                landmark_list.append((index, cx, cy))

        return landmark_list
