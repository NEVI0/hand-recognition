import cv2
import hand_tracking_module as htm


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = htm.HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        detector.find_position(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
