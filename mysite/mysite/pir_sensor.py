# publisher (pir 센서)

import threading
import paho.mqtt.client as mqtt
import time
import datetime

from gpiozero import MotionSensor, DistanceSensor

from picamera import PiCamera

from mysite.DAO import DataDAO

from subprocess import call

HOST = '192.168.35.71' # mqtt 브로커 주소 (pc)
PORT = 1883

topic = 'iot/monitor/pir'
msg = 'off'

class Pir(threading.Thread):
    def __init__(self, host, port, topic, msg):
        super().__init__()
        
        # pir 센서
        self.pir = MotionSensor(4)
        
        # 초음파 센서
        # self.ultra = DistanceSensor(24, 25, max_distance=1)
        # self.threshold_distance = 0.3

        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 25

        self.host = host
        self.port = port
        self.topic = topic
        self.msg = msg

        self.state = False # 초기 값

        self.client = mqtt.Client()
        self.client.connect(self.host, self.port)

        self.splitter_port = 2

        self.dao = DataDAO()

        self.fname = ""
        self.now = None
        
    def publish(self):
        self.client.publish(self.topic, self.msg)
        self.dao.insert_data(self.topic, self.msg)


    def run(self):
        time.sleep(5)
        while True:
            # 움직임이 감지되면

            # pir 센서
            if self.pir.motion_detected == True:

            # 초음파 센서
            # if self.ultra.distance <= self.threshold_distance:

                # pir 센서
                print("motion detected----------------")

                # 초음파 센서
                # print("motion detected----------------", self.ultra.distance)
                self.state = True
                self.msg = 'on'

                self.publish()

                if self.camera.recording == False:
                    print("start recording")
                    self.now = datetime.datetime.now() # 녹화 시작 시간
                    self.fname = self.now.strftime("%Y-%m-%d_%H:%M:%S") + '.mp4'
                    
                    # threading.Thread(target=self.camera.start_recording, kwargs={'output' : self.fname, 'splitter_port' : self.splitter_port}, daemon=True).start()
                    # h264 파일은 temp로 저장하고 녹화 종료 후에 fname.mp4로 변환
                    self.camera.start_recording("/home/pi/iot_workspace/smartdoor/iot-raspberry/mysite/media/"+ "temp.h264", splitter_port=2)
                
                time.sleep(5)

            # 움직임이 감지되지 않으면
            else:
                print("No motion !!!!!!!!!!!!!!!!!!!!!")
                self.state = False
                self.msg = 'off'
                
                self.publish()

                if self.camera.recording == True:
                    print("stop recording")
                    self.camera.stop_recording(splitter_port=2)

                    command = f"MP4Box -add /home/pi/iot_workspace/smartdoor/iot-raspberry/mysite/media/temp.h264 /home/pi/iot_workspace/smartdoor/iot-raspberry/mysite/media/{self.fname}"
                    call([command], shell=True)

                    self.dao.insert_recording_data(self.now, self.fname)
                
                time.sleep(1)


pir = Pir(HOST, PORT, topic, msg)
pir.daemon = True
pir.start()