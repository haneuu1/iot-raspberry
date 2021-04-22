# subscriber (서보 모터)

import paho.mqtt.client as mqtt

import pigpio

from datetime import datetime

from DAO import DataDAO
from audio import playsound
import time
from Keypad import *
import threading

HOST = '172.30.1.70'# pc
PORT = 1883
TOPIC = 'iot/control/#'

# 카메라 수직
SERVO_CAMERA_VERTICAL = 23
pi_camera_vertical = pigpio.pi()
pi_camera_vertical.set_servo_pulsewidth(SERVO_CAMERA_VERTICAL, 1500)

# # 카메라 수평
# SERVO_CAMERA_HORIZONTAL = 24
# pi_camera_horizontal = pigpio.pi()
# pi_camera_horizontal.set_servo_pulsewidth(SERVO_CAMERA_HORIZONTAL, 1500)

# # 도어락
# SERVO_DOOR = 18
# pi_door = pigpio.pi()
# pi_door.set_servo_pulsewidth(SERVO_DOOR, 1500)

dao = DataDAO()

def subscribe(host, port, topic, forever=True):

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

            pulse_width = 500 + 11.11*(value+90)
            pi_camera_vertical.set_servo_pulsewidth(SERVO_CAMERA_VERTICAL, pulse_width)
        
        # 카메라 서보 수평 제어
        if topic == 'iot/control/camera/servo/horizontal':
            value = int(message)

            pulse_width = 500 + 11.11*(value+90)
            pi_camera_horizontal.set_servo_pulsewidth(SERVO_CAMERA_HORIZONTAL, pulse_width)
        
        # 안드로이드에서 음성 요청
        if topic == 'iot/control/voice':            
            # 음성 합성 => 블루투스 스피커 연결시 초반 음 끊김... av jack은 정상 실행
            ##### PYTHON_LIB/audioapi.py의 API_KEY와 TTS_HEADERS. auth 변경 필요
            playsound(message, "MAN_DIALOG_BRIGHT")

        # 키패드 혹은 안드로이드에서 문 개방 요청
        if topic == 'iot/control/key':
            
            # DB에 저장
            dao.insert_data(topic, message)

            if message == 'on':
                pulse_width = 500 + 11.11*(90+90)
                pi_door.set_servo_pulsewidth(SERVO_DOOR, pulse_width)

                time.sleep(3)

                pulse_width = 500 + 11.11*(0+90)
                pi_door.set_servo_pulsewidth(SERVO_DOOR, pulse_width)

            else:
                # buzzer
                pass

        if topic == 'iot/control/key/temp':
            scl = 3
            sdo = 2
            keypad = Keypad(HOST, PORT, scl, sdo)
            ix = message.find('_')
            tpsd = message[0:ix]
            duration = int(message[ix+1:])
            print(f'temporary password: {tpsd}')
            print(f'duration: {duration}')
            t = threading.Thread(target=keypad.temp_run, args=(tpsd, duration))
            t.start()
            # keypad.temp_run(tpsd, duration)
            

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