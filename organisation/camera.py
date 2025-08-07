import cv2
import threading

class VideoCamera(object):
    def __init__(self):
        # You Can Commit Your CCTV Address in VideoCapture
        self.video = cv2.VideoCapture(0)
        (self.grabbed1, self.frame1) = self.video.read()
        self.frame1 = cv2.resize(self.frame1, (1280, 720))
        self.grabbed1 = cv2.resize(self.grabbed1, (1280, 720))
        self.frame = cv2.flip(self.frame1, 1)
        self.grabbed = cv2.flip(self.grabbed1, 1)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed1, self.frame1) = self.video.read()
            self.frame1 = cv2.resize(self.frame1, (1280, 720))
            self.grabbed1 = cv2.resize(self.grabbed1, (1280, 720))
            self.frame = cv2.flip(self.frame1, 1)
            self.grabbed = cv2.flip(self.grabbed1, 1)

def gen(camera):
    while True:
        frame = camera.get_frame()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')