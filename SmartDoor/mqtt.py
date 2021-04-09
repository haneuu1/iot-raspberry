from gpiozero import MotionSensor, LED
import pigpio
import paho.mqtt.client as mqtt
from mqtt_sub import subscribe
from datetime import datetime

##### 센서 설정
pir = MotionSensor(4)
led = LED(24)
SERVO = 22
pi = pigpio.pi() 
pi.set_servo_pulsewidth(SERVO, 1500)
# 서보 모터 지터링 방지
### 사용전 서버 데몬 기동 필요 $sudo pigpiod
### 정지 $sudo killall pigpiod

##### mqtt 설정
FILE_NAME = "test.txt"
HOST = "localhost"
# HOST = "192.168.35.71"
PORT = 1883
client = mqtt.Client()
client.connect(host=HOST, port=PORT)
def on_message(client, userdata, msg):
    with open(FILE_NAME, 'at') as f:
        f.write(f'{msg.topic}, {msg.payload}, {datetime.now()}\n')

        if msg.topic == 'iot/control/servo':
            print(f"{msg.topic} : {int(msg.payload)}")
            # value = int(msg.payload.decode('utf-8'))
            value = int(msg.payload)
            pulse_width = 500 + 11.11*(value+90)
            pi.set_servo_pulsewidth(SERVO, pulse_width)

        if msg.topic == 'iot/control/voice':
            print(f"{msg.topic} : {str(msg.payload)}")
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

def detected():
    print('motion detected!')
    led.on()
    client.publish('iot/monitor/pir', 'on')

def notdetected():
    print('motion not detected')
    led.off()
    client.publish('iot/monitor/pir', 'off')

def run():
    try:
        pir.when_motion = detected
        pir.when_no_motion = notdetected

        subscribe(HOST, 'iot/control/#', on_message)
        client.loop_forever()

    except Exception as e:
        print(e)

if __name__ == '__main__':
    run()