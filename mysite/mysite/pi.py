import paho.mqtt.client as mqtt_client
from mysite.DAO import DataDAO
from mysite.audio import playsound
from datetime import datetime
import random
from gpiozero import MotionSensor, LED, Servo
import pigpio

##### 센서 설정
pir = MotionSensor(4)
led = LED(21)
cam_servo = 23
key_servo = 24
pi = pigpio.pi()
pi.set_servo_pulsewidth(cam_servo, 1500)
pi.set_servo_pulsewidth(key_servo, 1500)
# 서보 모터 지터링 방지
### 사용전 서버 데몬 기동 필요 $sudo pigpiod
### 정지 $sudo killall pigpiod


class Pi:
    def __init__(self, shared_list):
        self.broker = "192.168.35.71" # 컴퓨터 ip - mqtt broker
        self.port = 1883
        self.input_topic = "iot/control/"
        # self.client_id = f'python-mqtt-{random.randint(0, 100)}'
        self.dao = DataDAO()
        self.topic = None
        self.msg = None
        self.shared_list = shared_list

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f'Connected with result code {rc}')
            else:
                print('연결 실패: ',rc)
        
        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, client: mqtt_client, topic, msg):
        client.publish(topic, msg)
        self.dao.insert_data(topic, msg)

    def subscribe(self, client: mqtt_client, topic):
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
            topic = msg.topic
            message = msg.payload.decode()
            # message = msg.payload.decode('utf-8')
            # message = msg.payload.decode('cp949')
            
            # self.dao.insert_data(topic, message.encode('utf-8', 'replace'))
            self.dao.insert_data(topic, message)

            if topic == 'iot/control/camera/servo':
                value = int(msg)
                pulse_width = 500 + 11.11*(value+90)
                pi.set_servo_pulsewidth(cam_servo, pulse_width)

            if topic == 'iot/control/voice':
                # 음성 합성 => 블루투스 스피커 연결시 초반 음 끊김... av jack은 정상 실행
                ##### PYTHON_LIB의 API_KEY와 TTS_HEADERS의 auth 변경 필요
                playsound(message)
                

            if topic == 'iot/control/key':
                value = msg.payload.decode('utf-8')
                if value == 'password':
                    # door open
                    pi.set_servo_pulsewidth(key_servo, 2500)
                else:
                    # buzzer
                    pass
        
        client.subscribe(topic)
        client.on_message = on_message
    
    def detected(self):
        print('motion detected!')
        led.on()
        self.publish(self.client, 'iot/monitor/pir', 'on')

    def notdetected(self):
        print('motion not detected')
        led.off()
        self.publish(self.client, 'iot/monitor/pir', 'off')
        
    def run(self):
        self.client = self.connect_mqtt()
        self.subscribe(self.client, 'iot/control/#')
        self.client.loop_start()
        
        # self.get_data()
        pir.when_motion = self.detected
        pir.when_no_motion = self.notdetected

        print('pi process start to run')
    
    def get_data(self):
        if ( (self.topic == None) & (self.msg == None)):
            return [0,0]
        else:
            return [self.topic, self.msg]

