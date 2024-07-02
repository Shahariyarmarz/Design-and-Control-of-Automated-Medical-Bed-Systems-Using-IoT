import RPi.GPIO as GPIO
import os
import requests
import bs4


res=requests.get('http://192.168.0.101:8000/contact/')
data= res.text
soup = bs4.BeautifulSoup(data,'lxml')
robotarray = soup.select('p')
robot=robotarray[16].getText()
print(robot)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
in1 = 17
in2 = 18
en = 5
in3 = 22
in4 = 27
enb = 6
GPIO.setup(en,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
pwma = GPIO.PWM(en,100)
pwmb = GPIO.PWM(enb,100)
pwma.start(0)
pwmb.start(0)



def printTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    print("GPU temperature is {}".format(temp[5:]))


def controlLED():
    try:
        

        if robot == 'val=C_251':
          GPIO.output(in1,GPIO.LOW)
          GPIO.output(in2,GPIO.HIGH)
          pwma.ChangeDutyCycle(50)
          GPIO.output(in3,GPIO.LOW)
          GPIO.output(in4,GPIO.HIGH)
          pwmb.ChangeDutyCycle(50)
          print("Forward is going")
        elif robot == 'val=C_250':
          GPIO.output(in1,GPIO.LOW)
          GPIO.output(in2,GPIO.LOW)
          pwma.ChangeDutyCycle(0)
          GPIO.output(in3,GPIO.LOW)
          GPIO.output(in4,GPIO.LOW)
          pwmb.ChangeDutyCycle(0)
          print("Break")
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("")


printTemperature()

controlLED()

