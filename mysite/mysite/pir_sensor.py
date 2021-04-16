# publisher (pir 센서)

from threading import Thread
import paho.mqtt.client as mqtt
import time
import datetime

from gpiozero import MotionSensor

from picamera import PiCamera

from mysite.DAO import DataDAO

from subprocess import call

HOST = '192.168.35.227' # mqtt 브로커 주소 (pc)
PORT = 1883

topic = 'iot/monitor/pir'
msg = 'off'

class Pir(Thread):
    def __init__(self, host, port, topic, msg):
        super().__init__()
        
        # pir 센서
        self.pir = MotionSensor(4)

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


    def detected(self):
        print('motion detected~~~~~~~~~~~~')

        self.state = True
        self.msg = 'on'

        self.publish()
        # self.client.publish(self.topic, self.msg)

        # 녹화 시작
        if self.camera.recording == False: # 녹화 중이 아니라면
            print("start recording")

            self.now = datetime.datetime.now() # 녹화 시작 시간
            self.fname = self.now.strftime("%Y_%m_%d_%H:%M:%S") + '.mp4'

            # self.dao.insert_recording_data(self.now, self.fname)
            
            # Thread(target=self.camera.start_recording, kwargs={'output' : self.fname, 'splitter_port' : self.splitter_port}, daemon=True).start()
            # h264 파일은 temp로 저장하고 녹화 종료 후에 fname.mp4로 변환
            self.camera.start_recording("/home/pi/iot_workspace/smartdoor/iot-raspberry/mysite/media/"+ "temp.h264", splitter_port=2)

        time.sleep(5) # 한 번 움직임이 감지되면 5초 녹화

    def not_detected(self):
        print('motion not detected^^^^^^^^^^^^^^')

        self.state = False
        self.msg = 'off'
        
        self.publish()
        # self.client.publish(self.topic, self.msg)

        # 녹화 중지
        if self.camera.recording == True: # 녹화 중이라면
            print("stop recording")
            
            # Thread(target=self.camera.stop_recording, kwargs={'splitter_port' : self.splitter_port}, daemon=True).start()
            self.camera.stop_recording(splitter_port=2)

            command = f"MP4Box -add /home/pi/iot_workspace/smartdoor/iot-raspberry/mysite/media/temp.h264 /home/pi/iot_workspace/smartdoor/iot-raspberry/mysite/media/{self.fname}"
            call([command], shell=True)

            self.dao.insert_recording_data(self.now, self.fname)

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
        #         self.msg = 'on'

        #         if (self.state == True) and (self.camera.recording == False):
        #             now = datetime.datetime.now()
        #             self.fname = now.strftime("%Y%m%d_%H%M") + '.h264'
        #             print("start recording")
        #             self.camera.start_recording(self.fname,splitter_port=2)

        #     else:
        #         self.state = False
        #         print("No motion !!!!!!!!!!!!!!!!!!!!!")
        #         self.msg = 'off'

        #         if (self.state == False) and (self.camera.recording == True):
        #             print("stop recording")
        #             self.camera.stop_recording(splitter_port=2)

time.sleep(3)

pir = Pir(HOST, PORT, topic, msg)
pir.daemon = True
pir.start()
