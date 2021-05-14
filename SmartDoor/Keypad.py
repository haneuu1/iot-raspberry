import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.client as mqtt
from gpiozero import Buzzer
import threading

HOST = # mqtt 브로커 주소 (pc)
PORT = 1883

class Keypad():
    # CONSTANTS
    KEYPAD = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]
    ]
    # 왼쪽부터 4개 핀
    ROW         = [18,23,24,25]
    # 그다음 4개 핀
    COLUMN      = [5,6,13,19]

    def __init__(self, host, port):
        GPIO.setmode(GPIO.BCM)

        self.buzzer = Buzzer(17)

        self.host = host
        self.port = port
        self.topic = 'iot/control/key'
        self.msg = 'on'

        self.client = mqtt.Client()
        self.client.connect(self.host, self.port)

        self.fname = 'doorlock.json'

        self.keyPressed = ''
        self.tempPeriod = True
        

    def getKey(self):
        keyVal = 0
        time.sleep(0.16)
        # Set all columns as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)

        # Set all rows as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Scan rows for pushed key/button
        # A valid key press should set "rowVal"  between 0 and 3.
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i

        # if rowVal is not 0 thru 3 then no button was pressed and we can exit
        if rowVal <0 or rowVal >3:
            self.exit()
            return

        # Convert columns to input
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Switch the i-th row found from scan to output
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)

        # Scan columns for still-pushed key/button
        # A valid key press should set "colVal"  between 0 and 3.
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal=j

        # if colVal is not 0 thru 3 then no button was pressed and we can exit
        if colVal < 0 or colVal > 3:
            self.exit()
            return

        # Return the value of the key pressed
        self.exit()

        keyVal = self.KEYPAD[rowVal][colVal]
        if keyVal!=self.keyPressed:
            self.keyPressed = keyVal
        return keyVal


    def exit(self):
        # Reinitialize all rows and columns as input at exit
        for i in range(len(self.ROW)):
                GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for j in range(len(self.COLUMN)):
                GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_password(self):
        with open(self.fname, 'r') as f:
            json_data = json.load(f)
            return json_data['password']
    
    def write_password(self, password):
        doorlock = dict()
        with open(self.fname, 'w', encoding="utf-8") as f:
            doorlock["password"] = password
            json.dump(doorlock, f, indent='\t')

    # 비밀번호 변경
    def set_password(self, input):
        ix = input.find('C')
        if input[:ix] == self.read_password():
            PASSWORD = input[ix+1:]
            self.write_password(PASSWORD)
            print(f'비밀번호 변경성공: {PASSWORD}')
            self.buzzer.beep(on_time=0.05, off_time=0.1, n=4)

        else:
            print('비밀번호 변경실패: Password Mismatched!')

    # 비밀번호 확인 중간에 #이 있는지
    def check_password(self, input):
        if input.find('C') != -1:
            return True
        else:
            return False

#####################일반 비밀번호            
    def input_password(self):
        input = ''
        start = False
        while True:
            key = self.getKey()
            if not key:
                continue
            if key == '*' and not start: # 시작
                start = True
                self.buzzer.beep(on_time=0.1, n =1)
                continue
            if key == '*' and start:
                print('reset')
                input = ''
                self.buzzer.beep(on_time=0.05, off_time=0.1, n=2)
                continue
            if not start: # 시작이 아니면 
                continue
            else: # 시작 이후의 키 입력
                print(f'key: {key}')
                if (key != '#'): # keypad 입력중
                    input += key
                    self.buzzer.beep(on_time=0.1, n =1)
                else: # keypad 입력 완료
                    print('입력완료', input)
                    return input
    
    def run(self):
        print('========start thread')
        while True:
            input = self.input_password()
            if (self.check_password(input)):
                self.set_password(input)
            else:
                if input == self.read_password():
                    print('open!')
                    self.client.publish(self.topic, self.msg) # 문열림
                    self.buzzer.beep(on_time=0.05, off_time=0.1, n=3)
                else:
                    print('Password Mismatched!')
                    self.buzzer.beep(on_time=1, n=1)
            input = ''

#####################임시 비밀번호
    def input_temp_password(self):
        input = ''
        start = False
        while self.tempPeriod:
            key = self.getKey()
            if not key:
                continue
            if key == '*' and not start: # 시작
                start = True
                self.buzzer.beep(on_time=0.1, n =1)
                continue
            if key == '*' and start:
                print('reset')
                input = ''
                self.buzzer.beep(on_time=0.05, off_time=0.1, n=2)
                continue
            if not start: # 시작이 아니면 
                continue
            else: # 시작 이후의 키 입력
                print(f'key: {key}')
                if (key != '#'): # keypad 입력중
                    input += key
                    self.buzzer.beep(on_time=0.1, n =1)
                else: # keypad 입력 완료
                    print('입력완료', input)
                    return input

    def temp_run(self, duration, temporary_key):
        t = threading.Timer(duration, self.tempOff)
        t.start()
        print('==start tempPeriod')
        while self.tempPeriod:
            if temporary_key == self.input_temp_password():
                # open
                self.client.publish(self.topic, self.msg)
                self.buzzer.beep(on_time=0.05, off_time=0.1, n=3)
            else:
                print('Password Mismatched!')
                self.buzzer.beep(on_time=1, n=1)
    
        print('==end tempPeriod')
        self.tempPeriod = True

    def tempOff(self):
        self.tempPeriod = False
        print(f'tempPeriod: {self.tempPeriod}')

keypad = Keypad(HOST, PORT)
if __name__ == '__main__':
    try:
        pass
        keypad.run()

    except KeyboardInterrupt:
            pass
            GPIO.cleanup()