#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer

"""No. of keys"""
inputKeys=16

GPIO.setmode(GPIO.BCM)
""" SCL and SDO pin can be any pin """
SCLPin=3
SDOPin=2
buzzer = Buzzer(12)
"""
Set SCL pin as OUTPUT
Set SDO pin as INPUT
"""

GPIO.setup(SCLPin,GPIO.OUT)
GPIO.setup(SDOPin,GPIO.IN)

keyPressed=0

def getKey():
        button=0
        global keyPressed
        keyState=0
        time.sleep(0.05)

        """
        Sample the Clock pin 16 times and read the data pin,
        when touched data pin is recorded LOW.
        """
        for i in range(inputKeys):
                GPIO.output(SCLPin,GPIO.LOW)
                if not GPIO.input(SDOPin):
                        keyState=i+1
                GPIO.output(SCLPin, GPIO.HIGH)
                
        if (keyState>0 and keyState!=keyPressed):
                button=keyState
                keyPressed=keyState
        else:
                keyPressed=keyState
        return (button)
        
        
try:
    # buzzer.beep(on_time=0.1, n =1) # 버튼입력할때
    # buzzer.beep(on_time=0.05, off_time=0.1, n=3) # 문이 열릴때
    buzzer.beep(on_time=1, n=1) # 비밀번호 틀렸을 때
    while True:
            key=getKey()
            if(key>0):
                    print(key)

except KeyboardInterrupt:
    pass
    GPIO.cleanup()
