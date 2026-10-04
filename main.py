import cv2

from hand_tracker import HandTracker
from mouse_controller import MouseController


def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Create objects
    tracker = HandTracker()
    mouse = MouseController()

    while True:
        success, frame = cap.read()

        if not success:
            print("Failed to read from webcam.")
            break

        # Flip frame for natural movement
        frame = cv2.flip(frame, 1)

        # Detect hand
        frame = tracker.find_hands(frame)

        # Get landmark positions
        landmarks = tracker.find_position(frame)

        # Perform mouse actions if hand detected
        if landmarks:
            mouse.update(frame, landmarks, tracker)

        # Display frame
        cv2.imshow("Virtual Mouse", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()