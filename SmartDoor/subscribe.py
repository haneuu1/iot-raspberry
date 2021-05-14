# subscriber (서보 모터)

# from gpiozero import AngularServo
import paho.mqtt.client as mqtt

import pigpio
from datetime import datetime

from DAO import DataDAO
from audio import playsound
import time
from keypad import keypad
import threading

HOST = # pc ip
PORT = 1883
TOPIC = 'iot/control/#'

pi = pigpio.pi() 

# 카메라 수직
SERVO_CAMERA_VERTICAL = 22
pi.set_servo_pulsewidth(SERVO_CAMERA_VERTICAL, 500)
# servo = AngularServo(20, min_angle=-90, max_angle=90, min_pulse_width = 0.0004, max_pulse_width = 0.0024)


# 카메라 수평
SERVO_CAMERA_HORIZONTAL = 27
pi.set_servo_pulsewidth(SERVO_CAMERA_HORIZONTAL, 1472)

# 도어락
SERVO_DOOR = 18
pi.set_servo_pulsewidth(SERVO_DOOR, 1472)

dao = DataDAO()
def subscribe(host, port, topic, forever=True):
    global tempPeriod
    tempPeriod = True

    def on_connect(client, userdata, flags, rc):
        print('Connected with result code', rc)
        if rc == 0:
            client.subscribe(topic) # 연결 성공 시 토픽 구독 신청
        else:
            print('연결 실패 : ', rc)

    def on_message(client, userdata, msg):
        print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")

        topic = msg.topic
        message = msg.payload.decode()
        # msg = msg.payload.decode('utf-8')
        
        # 카메라 서보 수직 제어
        if topic == 'iot/control/camera/servo/vertical':
            value = int(message)

            # servo.angle = value

            pulse_width = 500 + 11.11*(value+90)
            pi.set_servo_pulsewidth(SERVO_CAMERA_VERTICAL, pulse_width)
        
        # 카메라 서보 수평 제어
        if topic == 'iot/control/camera/servo/horizontal':
            value = int(message)

            pulse_width = 600 + 10*(value+90)
            pi.set_servo_pulsewidth(SERVO_CAMERA_HORIZONTAL, pulse_width)
        
        # 안드로이드에서 음성 요청
        if topic == 'iot/control/voice':            
            # 음성 합성 => 블루투스 스피커 연결시 초반 음 끊김... av jack은 정상 실행
            ##### PYTHON_LIB/audioapi.py의 API_KEY와 TTS_HEADERS. auth 변경 필요
            playsound(message, "MAN_DIALOG_BRIGHT")

        # 키패드 혹은 안드로이드에서 문 개방 요청
        if topic == 'iot/control/key':
            
            # DB에 저장
            dao.insert_data(topic, message)

            if message == 'direct_on' or message == 'app_on' or message == 'temp_on':
                pulse_width = 500 + 11.11*(90+90)
                pi.set_servo_pulsewidth(SERVO_DOOR, pulse_width)

                time.sleep(5)

                pulse_width = 500 + 11.11*(0+90)
                pi.set_servo_pulsewidth(SERVO_DOOR, pulse_width)

            else:
                # buzzer
                pass

        if topic == 'iot/control/key/temp':
            ix = message.find('_')
            tpsd = message[0:ix]
            duration = int(message[ix+1:])
            
            print(f'temporary password: {tpsd}')
            print(f'duration: {duration}')

            t = threading.Thread(target=keypad.temp_run, args=(duration, tpsd))
            t.start()
            

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port)

    if forever:
        client.loop_forever()
    else:
        client.loop_start()



if __name__ == "__main__":
    subscribe(HOST, PORT, TOPIC)