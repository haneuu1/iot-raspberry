import RPi.GPIO as GPIO
import time
import json

"""No. of keys"""
inputKeys=16

GPIO.setmode(GPIO.BCM)
""" SCL and SDO pin can be any pin """
SCLPin=16
SDOPin=20

"""
Set SCL pin as OUTPUT
Set SDO pin as INPUT
"""

GPIO.setup(SCLPin,GPIO.OUT)
GPIO.setup(SDOPin,GPIO.IN)

keyPressed=0
input = ''
PASSWORD = ''

def getKey():
    button=''
    global keyPressed
    keyState=0
    time.sleep(0.05)

    # """
    # Sample the Clock pin 16 times and read the data pin,
    # when touched data pin is recorded LOW.
    # """
    for i in range(inputKeys):
        GPIO.output(SCLPin,GPIO.LOW)
        if not GPIO.input(SDOPin):
                keyState=i+1
        GPIO.output(SCLPin, GPIO.HIGH)
            
    if (keyState>0 and keyState!=keyPressed):
        # print(f'keyState: {keyState}')
        # print(f'keyPressed: {keyPressed}')
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
        keyPressed=keyState
    else:
        keyPressed=keyState
    return button
    
def read_password():
    with open('doorlock.json', 'r') as f:
        json_data = json.load(f)
        # print(json.dumps(json_data['password']))
        return json_data

def write_password(password):
    doorlock = dict()
    with open('doorlock.json', 'w', encoding="utf-8") as f:
        doorlock["password"] = password
        doorlock["length"] = len(password)
        json.dump(doorlock, f, indent='\t')
 
try:
    while True:
        key=getKey()
        if key:
            if (key != 'd'): # keypad 입력중
                input += key
            else: # keypad 입력 완료
                print(f'input: {input}')
                if input[0] == 'a': # 번호 입력 시작
                    print(f'input: {input}')
                    if input[1:] == read_password()['password']:
                        print('open!')
                        # 문 열림

                    elif (input[1:read_password()['length']+1] == read_password()['password'] and input[read_password()['length']+1] == '#'):
                        PASSWORD = input[read_password()['length']+2:]
                        write_password(PASSWORD)
                        print(f'비밀번호 변경: {PASSWORD}')

                # elif input[0]=='#': # 새로운 비밀번호 입력 시작
                #     PASSWORD = input[1:]
                #     write_password(PASSWORD)
                
                input = ''

            
except KeyboardInterrupt:
    pass
    GPIO.cleanup()
