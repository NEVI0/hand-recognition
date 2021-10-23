import cv2
import sys
import math
import keyboard
import hand_detector as hd
import volume_controller as vc

RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
ORANGE_COLOR = (0, 127, 255)

FONT_FAMILY = cv2.FONT_HERSHEY_SIMPLEX
FONT_LINE = cv2.LINE_AA
FONT_SCALE = 0.75
FONT_SIZE = 2

MODES = [
    {'name': 'Counter', 'key': '1'},
    {'name': 'Volume Controller', 'key': '2'},
    {'name': 'Object Moving', 'key': '3'}
]


def main():
    use_analytic_mode = 'Y'
    # use_analytic_mode = input(' - Do you want to use analytic mode? (Y / n) ')

    if use_analytic_mode == 'Y' or use_analytic_mode == 'y':
        print(' - Press "X" button to stop running!')
    else:
        print(' - Press "Ctrl + C" to stop running!')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = hd.HandDetector()
    volume = vc.VolumeController()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        landmark_list = detector.find_position(img)

        if len(landmark_list) > 0:

            finger_1 = (landmark_list[4][1], landmark_list[4][2])
            finger_2 = (landmark_list[8][1], landmark_list[8][2])

            between_fingers = ((finger_1[0] + finger_2[0]) // 2, (finger_1[1] + finger_2[1]) // 2)

            cv2.circle(img, between_fingers, 8, RED_COLOR, cv2.FILLED)
            cv2.circle(img, finger_1, 8, ORANGE_COLOR, cv2.FILLED)
            cv2.circle(img, finger_2, 8, ORANGE_COLOR, cv2.FILLED)

            cv2.line(img, finger_1, finger_2, ORANGE_COLOR, 4)

            length = math.hypot(finger_2[0] - finger_1[0], finger_2[1] - finger_1[1])
            volume.set_volume(length)

        if keyboard.is_pressed('1'):
            print('Key "1" was pressed!')

        if use_analytic_mode == 'Y' or use_analytic_mode == 'y':
            cv2.putText(img, 'Analytic Mode', (10, 30), FONT_FAMILY, FONT_SCALE, GREEN_COLOR, FONT_SIZE, FONT_LINE)

            cv2.imshow("Analytic Camera Mode", img)
            cv2.waitKey(1)

            if cv2.getWindowProperty('Analytic Camera Mode', cv2.WND_PROP_VISIBLE) < 1:
                break

    cv2.destroyAllWindows()
    sys.exit()


if __name__ == '__main__':
    main()
