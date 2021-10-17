import cv2, math
import hand_tracking_module as htm


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = htm.HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        landmark_list = detector.find_position(img)

        if len(landmark_list) > 0:

            finger_1 = (landmark_list[4][1], landmark_list[4][2])
            finger_2 = (landmark_list[8][1], landmark_list[8][2])

            center_line = ((finger_1[0] + finger_2[0]) // 2, (finger_1[1] + finger_2[1]) // 2)

            cv2.circle(img, center_line, 8, (52, 229, 132), cv2.FILLED)
            cv2.circle(img, finger_1, 8, (52, 229, 132), cv2.FILLED)
            cv2.circle(img, finger_2, 8, (52, 229, 132), cv2.FILLED)

            cv2.line(img, finger_1, finger_2, (52, 229, 132), 4)

            length = math.hypot(finger_2[0] - finger_1[0], finger_2[1] - finger_1[1])

            if length > 150:
                cv2.circle(img, center_line, 8, (224, 53, 53), cv2.FILLED)

            if length < 50:
                cv2.circle(img, center_line, 8, (226, 148, 52), cv2.FILLED)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
