import math
from constants import *


class ModeController:
    def __init__(self):
        pass

    @staticmethod
    def display_selected_mode(img, mode):
        cv2.putText(img, 'Analytic Mode', (10, 30), FONT_FAMILY, FONT_SCALE, GREEN_COLOR, FONT_SIZE, FONT_LINE)

        counter_text = 'Counter: 1'
        volume_text = 'Volume Controller: 2'
        object_text = 'Object Moving: 3'

        if mode == 1:
            counter_text = counter_text.replace('1', 'Selected')
        if mode == 2:
            volume_text = volume_text.replace('2', 'Selected')
        if mode == 3:
            object_text = object_text.replace('3', 'Selected')

        cv2.putText(img, counter_text, (10, 385), FONT_FAMILY, FONT_SCALE, BLUE_COLOR, FONT_SIZE, FONT_LINE)
        cv2.putText(img, volume_text, (10, 425), FONT_FAMILY, FONT_SCALE, BLUE_COLOR, FONT_SIZE, FONT_LINE)
        cv2.putText(img, object_text, (10, 465), FONT_FAMILY, FONT_SCALE, BLUE_COLOR, FONT_SIZE, FONT_LINE)

    @staticmethod
    def use_counter_mode(img, landmark_list):
        founded_fingers = []

        if landmark_list[FINGERS[0]][1] < landmark_list[FINGERS[0] - 1][1]:
            founded_fingers.append(1)
        else:
            founded_fingers.append(0)

        for index in range(1, 5):
            if landmark_list[FINGERS[index]][2] < landmark_list[FINGERS[index] - 2][2]:
                founded_fingers.append(1)
            else:
                founded_fingers.append(0)

        fingers_counted = str(founded_fingers.count(1))
        cv2.putText(img, fingers_counted, (530, 465), FONT_FAMILY, 5, WHITE_COLOR, 10, FONT_LINE)

    @staticmethod
    def use_volume_mode(img, volume_ctrl, landmark_list):
        finger_1 = (landmark_list[4][1], landmark_list[4][2])
        finger_2 = (landmark_list[8][1], landmark_list[8][2])

        between_fingers = ((finger_1[0] + finger_2[0]) // 2, (finger_1[1] + finger_2[1]) // 2)

        cv2.circle(img, between_fingers, 8, RED_COLOR, cv2.FILLED)
        cv2.circle(img, finger_1, 8, ORANGE_COLOR, cv2.FILLED)
        cv2.circle(img, finger_2, 8, ORANGE_COLOR, cv2.FILLED)

        cv2.line(img, finger_1, finger_2, ORANGE_COLOR, 4)

        length = math.hypot(finger_2[0] - finger_1[0], finger_2[1] - finger_1[1])
        volume_bar = volume_ctrl.set_volume(length)
        volume_ctrl.display_volume_bar(img, volume_bar)

    @staticmethod
    def use_object_moving_mode(img):
        cv2.rectangle(img, (250, 250), (300, 300), (255, 255, 255), -1)
