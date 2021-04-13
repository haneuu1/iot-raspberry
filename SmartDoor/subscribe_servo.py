# subscriber (서보 모터)

import paho.mqtt.client as mqtt

import pigpio

from datetime import datetime

import requests

HOST = '192.168.35.28'
PORT = 1883
TOPIC = 'iot/control/#'

SERVO = 17
pi = pigpio.pi() 
pi.set_servo_pulsewidth(SERVO, 1500)
# 서보 모터 지터링 방지
### 사용전 서버 데몬 기동 필요 $sudo pigpiod
### 정지 $sudo killall pigpiod

FILE_NAME = "test.txt"

def subscribe_servo(host, port, topic, forever=True):

    def on_connect(client, userdata, flags, rc):
        print('Connected with result code', rc)
        if rc == 0:
            client.subscribe(topic) # 연결 성공 시 토픽 구독 신청
        else:
            print('연결 실패 : ', rc)

    def on_message(client, userdata, msg):
        # 구독한 메세지 모두 파일로 저장
        with open(FILE_NAME, 'at') as f:
            f.write(f'{msg.topic}, {msg.payload}, {datetime.now()}\n')

            if msg.topic == 'iot/control/camera/servo':
                print(f"{msg.topic} : {int(msg.payload)}")
                # value = int(msg.payload.decode('utf-8'))
                value = int(msg.payload)
                pulse_width = 500 + 11.11*(value+90)
                pi.set_servo_pulsewidth(SERVO, pulse_width)

            if msg.topic == 'iot/control/voice':
                print(f"{msg.topic} : {str(msg.payload)}")
                # r = requests.get("http://192.168.35.41:8000/mqtt/pir/")
                # print(r.content)
                
                # 음성 합성

            if msg.topic == 'iot/control/key':
                print(f"{msg.topic} : {int(msg.payload)}")
                value = str(msg.payload)
                if value == 'password':
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
    subscribe_servo(HOST, PORT, TOPIC)