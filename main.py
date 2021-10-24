import sys
import keyboard
import hand_detector as hd
import volume_controller as vc
import mode_controller as mc

from constants import *


def main():
    selected_mode = 1
    use_analytic_mode = input(' - Do you want to use analytic mode? (Y / n) ')

    if use_analytic_mode == 'Y' or use_analytic_mode == 'y':
        print(' - Press "X" button to stop running!')
    else:
        print(' - Press "Ctrl + C" to stop running!')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = hd.HandDetector()
    volume_ctrl = vc.VolumeController()
    mode_ctrl = mc.ModeController()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        landmark_list = detector.find_position(img)

        if len(landmark_list) > 0:
            if selected_mode == 1:
                mode_ctrl.use_counter_mode(img, landmark_list)
            if selected_mode == 2:
                mode_ctrl.use_volume_mode(img, volume_ctrl, landmark_list)
            if selected_mode == 3:
                mode_ctrl.use_object_moving_mode(img)
        else:
            cv2.putText(img, 'Hand not Detected', (200, 235), FONT_FAMILY, FONT_SCALE, RED_COLOR, FONT_SIZE, FONT_LINE)

        if keyboard.is_pressed('1'):
            selected_mode = 1
        if keyboard.is_pressed('2'):
            selected_mode = 2
        if keyboard.is_pressed('3'):
            selected_mode = 3

        if use_analytic_mode == 'Y' or use_analytic_mode == 'y':

            mode_ctrl.display_selected_mode(img, selected_mode)
            cv2.imshow(WINDOW_NAME, img)
            cv2.waitKey(1)

            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break

    cv2.destroyAllWindows()
    sys.exit()


if __name__ == '__main__':
    main()
