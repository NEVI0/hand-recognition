import cv2
import sys
import math
import numpy as np
import hand_tracking_module as htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

RED_COLOR = (0, 0, 255)
ORANGE_COLOR = (0, 127, 255)


def main():
    use_analytic_mode = input(' - Do you want to use analytic mode? (Y / n) ')

    if use_analytic_mode == 'Y' or use_analytic_mode == 'y':
        print(' - Press "X" button to stop running!')
    else:
        print(' - Press "Ctrl + C" to stop running!')

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_controller = cast(interface, POINTER(IAudioEndpointVolume))

    vol_range = volume_controller.GetVolumeRange()
    min_vol, max_vol = vol_range[0], vol_range[1]

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = htm.HandDetector()

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

            volume = np.interp(length, [50, 250], [min_vol, max_vol])
            volume_controller.SetMasterVolumeLevel(volume, None)

        if use_analytic_mode == 'Y' or use_analytic_mode == 'y':
            cv2.imshow("Analytic Camera Mode", img)
            cv2.waitKey(1)

            if cv2.getWindowProperty('Analytic Camera Mode', cv2.WND_PROP_VISIBLE) < 1:
                break

    cv2.destroyAllWindows()
    sys.exit()


if __name__ == '__main__':
    main()
