from picamera import PiCamera
import io
import time

class PiCam:
    def __init__(self, camera, show=True, framerate=25, width=640, height=480):
        self.size = (width, height)
        self. show = show
        self.framerate = framerate

        # self.camera = PiCamera()
        self.camera = camera

        self.camera.rotation = 180
        self.camera.resolution = self.size
        self.camera.framerate = self.framerate


class MJpegStreamCam(PiCam):
    def __init__(self, camera, show=True, framerate=25, width=640, height=480):
        super().__init__(camera=camera, show=show, framerate=framerate, width=width, height=height)

    def __iter__(self):
        frame = io.BytesIO()
        while True:
            self.camera.capture(frame, format="jpeg", use_video_port=True, splitter_port=1)
            image = frame.getvalue()
            yield (b'--myboundary\n'
                    b'Content-Type::image/jpeg\n'
                    b'Content-Length: ' + f"{len(image)}".encode() + b'\n'
                    b'\n' + image + b'\n')
            frame.seek(0)
            time.sleep(1/self.framerate)
    
    def __del__(self):
        self.camera.close()
            