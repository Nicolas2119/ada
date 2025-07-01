import cv2


def open():
    """Open the default camera feed and display it until ``q`` is pressed."""

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Could not open camera."

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cv2.destroyAllWindows()
                return "Error: Could not read frame."

            cv2.imshow("Camera Feed", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return "Camera closed"
