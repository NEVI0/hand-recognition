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
        size = FONT_SIZE - 1
        scale = FONT_SCALE - 0.10

        if len(landmark_list[4]) > 0:
            finger_1 = (landmark_list[4][1] - 5, landmark_list[4][2] - 15)
            cv2.putText(img, '1', finger_1, FONT_FAMILY, scale, WHITE_COLOR, size, FONT_LINE)

        if len(landmark_list[8]) > 0:
            finger_2 = (landmark_list[8][1] - 5, landmark_list[8][2] - 15)
            cv2.putText(img, '2', finger_2, FONT_FAMILY, scale, WHITE_COLOR, size, FONT_LINE)

        if len(landmark_list[12]) > 0:
            finger_3 = (landmark_list[12][1] - 5, landmark_list[12][2] - 15)
            cv2.putText(img, '3', finger_3, FONT_FAMILY, scale, WHITE_COLOR, size, FONT_LINE)

        if len(landmark_list[16]) > 0:
            finger_4 = (landmark_list[16][1] - 5, landmark_list[16][2] - 15)
            cv2.putText(img, '4', finger_4, FONT_FAMILY, scale, WHITE_COLOR, size, FONT_LINE)

        if len(landmark_list[20]) > 0:
            finger_5 = (landmark_list[20][1] - 5, landmark_list[20][2] - 15)
            cv2.putText(img, '5', finger_5, FONT_FAMILY, scale, WHITE_COLOR, size, FONT_LINE)

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
