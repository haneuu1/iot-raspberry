# subscriber (서보 모터)

import paho.mqtt.client as mqtt

import pigpio

from datetime import datetime

from DAO import DataDAO
from audio import playsound

HOST = '192.168.35.227'# pc
PORT = 1883
TOPIC = 'iot/control/#'

SERVO = 23
pi = pigpio.pi() 
pi.set_servo_pulsewidth(SERVO, 1500)
# 서보 모터 지터링 방지
### 사용전 서버 데몬 기동 필요 $sudo pigpiod
### 정지 $sudo killall pigpiod

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
        

        if topic == 'iot/control/camera/servo':
            value = int(message)
            pulse_width = 500 + 11.11*(value+90)
            pi.set_servo_pulsewidth(SERVO, pulse_width)

        if topic == 'iot/control/voice':            
            # 음성 합성 => 블루투스 스피커 연결시 초반 음 끊김... av jack은 정상 실행
            ##### PYTHON_LIB/audioapi.py의 API_KEY와 TTS_HEADERS. auth 변경 필요
            playsound(message, "MAN_DIALOG_BRIGHT")

        if topic == 'iot/control/key':
            dao.insert_data(topic, message)

            if message == 'password':
                # door open
                pass
            else:
                # buzzer
                pass

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