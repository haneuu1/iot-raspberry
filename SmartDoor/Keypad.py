import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.client as mqtt

# 임시키
# topic: iot/control/key/temp
# msg: '0000_20' 

HOST = '172.30.1.70' # mqtt 브로커 주소 (pc)
PORT = 1883

SCLPin = 3
SDOPin = 2


class Keypad():
    def __init__(self, host, port, scl, sdo):
        super().__init__()

        self.host = host
        self.port = port
        self.topic = 'iot/control/key'
        self.msg = 'on'

        self.client = mqtt.Client()
        self.client.connect(self.host, self.port)

        self.scl = scl
        self.sdo = sdo

        self.fname = 'doorlock.json'
        self.inputKeys = 16
        self.keyPressed = 0
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.scl, GPIO.OUT)
        GPIO.setup(self.sdo, GPIO.IN)

    def getKey(self):
        
        button=''
        # self.keyPressed
        keyState = 0
        time.sleep(0.05)
        
        for i in range(self.inputKeys):
            GPIO.output(self.scl,GPIO.LOW)
            if not GPIO.input(self.sdo):
                    keyState=i+1
            GPIO.output(self.scl, GPIO.HIGH)
        # print(f'keystate: {keyState}')
        if (keyState>0 and keyState!=self.keyPressed):
            if(keyState < 10) : button += str(keyState)
            elif(keyState == 10) : button = '0'
            elif(keyState == 11) : button = '*' 
            elif(keyState == 12) : button = '#' 
            elif(keyState == 13) : button = 'a' 
            elif(keyState == 14) : button = 'b' 
            elif(keyState == 15) : button = 'c' 
            elif(keyState == 16) : button = 'd'
            else:
                button= None
            self.keyPressed=keyState
            
        else:
            self.keyPressed=keyState
        # print(f'keyPressed: {self.keyPressed}')
        return button

    def input_password(self): # return input
        input = ''
        print('start input===')
        start = False
        while True:
            key=self.getKey()
            if not key : continue

            if key == 'a' and not start: # 시작
                start = True
                continue
            
            if key == 'a' and start:
                input = ''
                continue

            if not start: # 시작이 아니면 
                continue

            else: # 시작 이후의 키 입력
                print(f'key: {key}')
                
                if (key != 'd'): # keypad 입력중
                    input += key
                    # print(key, input)

                else: # keypad 입력 완료
                    print('입력완료', input)
                    return input
   
    def read_password(self):
        with open(self.fname, 'r') as f:
            json_data = json.load(f)
            # print(json.dumps(json_data['password']))
            return json_data['password']
        
    def write_password(self, password):
        doorlock = dict()
        with open(self.fname, 'w', encoding="utf-8") as f:
            doorlock["password"] = password
            doorlock["length"] = len(password)
            json.dump(doorlock, f, indent='\t')

    # 비밀번호 변경
    def set_password(self, input):
        ix = input.find('#')
        if input[:ix] == self.read_password():
            PASSWORD = input[ix+1:]
            self.write_password(PASSWORD)
            print(f'비밀번호 변경성공: {PASSWORD}')
        else:
            print('비밀번호 변경실패: Password Mismatched!')

    # 비밀번호 확인 중간에 #이 있는지
    def check_password(self, input):
        if input.find('#') != -1:
            return True
        else:
            return False

    def run(self):
        while True:
            input = self.input_password()
            if (self.check_password(input)):
                self.set_password(input)
            else:
                if input == self.read_password():
                    print('open!')
                    self.client.publish(self.topic, self.msg) # 문열림
                else:
                    print('Password Mismatched!')
            input = ''


    def temp_run(self, temporary_key, duration):
        t_end = time.time() + duration
        print(f'start timer: {duration}s')
        while time.time() < t_end:
            if temporary_key == self.input_password():
                # open
                self.client.publish(self.topic, self.msg)
            else:
                print('Password Mismatched!')
        print('end timer')


if __name__ == "__main__":
    try:
        keypad = Keypad(HOST, PORT, SCLPin, SDOPin)
        keypad.run()
        # a = keypad.input_password()
        # print(a)

    except KeyboardInterrupt:
        pass
        GPIO.cleanup()
    # finally:
    #     GPIO.cleanup()