import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import os
import requests
import bs4

# Software SPI configuration:


CLK  = 23
MISO = 21
MOSI = 19
CS   = 24
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
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

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
 
print('Reading MCP3008 values, press Ctrl-C to quit...')

# Main program loop.

def printTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    print("GPU temperature is {}".format(temp[5:]))


def controlLED():
    try:
        while True:
            res=requests.get('http://192.168.0.100:8000/contact/')
            data= res.text
            soup = bs4.BeautifulSoup(data,'lxml')
            robotarray = soup.select('p')
            robot=robotarray[16].getText()
            print(robot)
            s3=mcp.read_adc(3);
            print(s3)
            if robot == 'val=C_251':
                if s3<700:
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.HIGH)
                    pwma.ChangeDutyCycle(95)
                    GPIO.output(in3,GPIO.LOW)
                    GPIO.output(in4,GPIO.HIGH)
                    pwmb.ChangeDutyCycle(35)
                    print("Forward going")
                else:
                    GPIO.output(in1,GPIO.LOW)
                    GPIO.output(in2,GPIO.LOW)
                    pwma.ChangeDutyCycle(0)
                    GPIO.output(in3,GPIO.LOW)
                    GPIO.output(in4,GPIO.LOW)
                    pwmb.ChangeDutyCycle(0)
                    print("Break")
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