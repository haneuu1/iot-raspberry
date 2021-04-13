# publisher (pir 센서)

from threading import Thread
import paho.mqtt.client as mqtt
import time
import datetime

from gpiozero import MotionSensor, DistanceSensor

from picamera import PiCamera

HOST = '192.168.35.28' # mqtt 브로커 주소 (pc)
PORT = 1883

topic = 'iot/monitor/pir'
value = 'off'

class Pir(Thread):
    def __init__(self, host, port, topic, value):
        super().__init__()
        
        # pir 센서
        self.pir = MotionSensor(4)
        
        # 초음파 센서
        # self.pir = DistanceSensor(23, 24, max_distance=1, threshold_distance=0.5)

        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 25

        self.host = host
        self.port = port
        self.topic = topic
        self.value = value

        self.state = False # 초기 값

        self.client = mqtt.Client()
        self.client.connect(self.host, self.port)

        self.splitter_port = 2

    def detected(self):
        # pir 센서
        print('motion detected~~~~~~~~~~~~')
        # 초음파 센서
        # print('motion detected~~~~~~~~~~~~', self.pir.distance)

        self.state = True
        self.value = 'on'
        self.client.publish(self.topic, self.value)

        # 녹화 시작
        if (self.state == True) and (self.camera.recording == False):
            now = datetime.datetime.now()
            fname = now.strftime("%Y%m%d_%H%M") + '.h264'
            print("start recording")
            
            # Thread(target=self.camera.start_recording, kwargs={'output' : fname, 'splitter_port' : self.splitter_port}, daemon=True).start()
            self.camera.start_recording(fname, splitter_port=2)

        time.sleep(5)

    def not_detected(self):
        # pir 센서
        print('motion not detected^^^^^^^^^^^^^^')
        # 초음파 센서
        # print('motion not detected^^^^^^^^^^^^^^', self.pir.distance)

        self.state = False
        self.value = 'off'
        self.client.publish(self.topic, self.value)

        # 녹화 중지
        if (self.state == False) and (self.camera.recording == True):
            print("stop recording")
            
            # Thread(target=self.camera.stop_recording, kwargs={'splitter_port' : self.splitter_port}, daemon=True).start()
            self.camera.stop_recording(splitter_port=2)

        time.sleep(1)
        

    def run(self):
        try:
            # pir 센서
            self.pir.when_motion = self.detected
            self.pir.when_no_motion = self.not_detected

            # 초음파 센서
            # self.pir.when_in_range = self.detected
            # self.pir.when_out_of_range = self.not_detected

        except Exception as e:
            print(e)
        
        # while True:
        #     if self.pir.motion_detected == True:
        #         self.state = True
        #         print("motion detected----------------")
        #         self.value = 'on'

        #         if (self.state == True) and (self.camera.recording == False):
        #             now = datetime.datetime.now()
        #             fname = now.strftime("%Y%m%d_%H%M") + '.h264'
        #             print("start recording")
        #             self.camera.start_recording(fname,splitter_port=2)

        #     else:
        #         self.state = False
        #         print("No motion !!!!!!!!!!!!!!!!!!!!!")
        #         self.value = 'off'

        #         if (self.state == False) and (self.camera.recording == True):
        #             print("stop recording")
        #             self.camera.stop_recording(splitter_port=2)


pir = Pir(HOST, PORT, topic, value)
pir.daemon = True
pir.start()