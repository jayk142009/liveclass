import cv2
import datetime

class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.is_recording = False
        self.out = None

    def __del__(self):
        self.cap.release()
        if self.out:
            self.out.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            if self.is_recording and self.out:
                self.out.write(frame)
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        return None

    def start_recording(self):
        if not self.is_recording:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.avi")
            self.out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            self.is_recording = True

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            if self.out:
                self.out.release()
                self.out = None
    
