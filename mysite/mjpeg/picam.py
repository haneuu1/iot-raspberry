import cv2
import io
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera, PiCameraCircularIO
import datetime
import random

savepath = '/home/pi/Desktop/cctv recording'

class PiCam:
    def __init__(self, show=True, framerate=25, width=640, height=480):
        self.size = (width, height)
        self. show = show
        self.framerate = framerate

        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = self.size
        self.camera.framerate = self.framerate

        def __iter__(self):
            rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
            rawCapture.truncate(0)
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

                yield frame.array
                rawCapture.truncate(0)

                def run(self, callback=None):
                    rawCapture = PiRGBArray(self.camera, size=self.camera.resolution)
                    rawCapture.truncate(0)
                    for frame in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

                        image = frame.array
                        if callback and not callback(image): break
                        if(self.show or callback == None):
                            cv2.imshow('frame', image)
                            key = cv2.waitKey(1)
                            if key == 27:break
                            rawCapture.truncate(0)

                        cv2.destroyAllWindows()

        def motion_detected(self):
            return random.randint(0, 10) == 0

        camera = PiCamera()
        stream = PiCameraCircularIO(camera, seconds=10)
        camera.resolution = (640, 480)
        now = datetime.datetime.now()
        filename = now.strftime('%Y-%m-%d %H:#M:%S')
        camera.start_recording(stream, format='h264')
        try:
            while True:
                camera.wait_recording(1)
                if motion_detected():
                    camera.wait_recording(10)
                    stream.copy_to(output = savepath + "/" + filename + '.h264')

        finally:
            camera.stop_recording()



class MJpegStreamCam(PiCam):
    def __init__(self, show=True, framerate=25, width=640, height=480):
        super().__init__(show=show, framerate=framerate, width=width, height=height)

    def __iter__(self):
        frame = io.BytesIO()
        while True:
            self.,camera.capture(frame, format="jpeg", use_video_port=True)
            image = frame.getvalue()
            yield (b'--myboundary\n'
                    b'Content-Type::image/jpeg\n'
                    b'Content-Length: ' + f"{len(image)}.encode() + b'/n'"
                    b'\n' + image + b'\n')
            frame.seek(0)
            