import cv2
import os
from datetime import datetime

class CameraRecorder:
    def capture_once(self):
        os.makedirs("data/evidence", exist_ok=True)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[CAMERA] Camera not accessible")
            return None

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("[CAMERA] Capture failed")
            return None

        filename = datetime.now().strftime("image_%Y%m%d_%H%M%S.jpg")
        path = os.path.join("data/evidence", filename)
        cv2.imwrite(path, frame)

        print(f"[CAMERA] Captured {filename}")
        return path
