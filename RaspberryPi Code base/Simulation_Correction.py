# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import os
import requests
import bs4
import time


# Software SPI configuration:
CLK  = 23
MISO = 21
MOSI = 19
CS   = 24
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#Motor pin define
motorpin1A=17
motorpin2A=18
motorpin1B=22
motorpin2B=27
enaA=5
enaB=6

GPIO.setup(motorpin1A,GPIO.OUT)
GPIO.setup(motorpin2A,GPIO.OUT)
GPIO.setup(motorpin1B,GPIO.OUT)
GPIO.setup(motorpin2B,GPIO.OUT)
GPIO.setup(enaA,GPIO.OUT)
GPIO.setup(enaB,GPIO.OUT)

#PWM pin define
pwmA = GPIO.PWM(enaA, 100) # GPIO enaA for PWM with 500Hz
pwmA.start(0)
pwmB = GPIO.PWM(enaB, 100) # GPIO enaB for PWM with 500Hz
pwmB.start(0)


# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
print('Reading MCP3008 values, press Ctrl-C to quit...')


#Constant Variable
error=0
prevError=0
contiBlack=35
mappedValue=7
targetValue=7
safety=0.35
kp=50
kd=200
time=3
maxSpeed=100
sensorNum=8


#IR List
IR_array = [0]*sensorNum
"""solve blacklimit list problem"""
blackLimit = [0]*sensorNum 



# Main program loop and function.
def IRread():
    #global IR_array
    for i in range(0,sensorNum):
        IR_array[i] = mcp.read_adc(i)
    #print('| {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*IR_array))
    #time.sleep(0.5)

def sensorMapping ():
    global stopcounter
    global mappedValue
    Sum=0
    Coun=0
    global sensorNum
    sensorNum = 8
    IRread()
    for i in range(0, sensorNum):
        print("IR array value")
        print(IR_array[i])
        print("black limit")
        print(blackLimit[i])
        if(IR_array[i]<blackLimit[i]):
            Sum += i*2
            Coun += 1
    if(Coun != 0):
        mappedValue = Sum/Coun
    else:
        mappedValue = 0
        print("else mappedValue")
    
    
    if(Coun<8):
        stopcounter = 0
        
    if(Coun==8):
        stopcounter += 1
        
def pid():
    #Localerror solve
    global error
    global prevError
    global leftSpeed
    global rightSpeed
    error=targetValue-mappedValue
    correction=(kp*error)+(kd*(error-prevError))
    prevError=error
    motorResponse=int(correction)
    if(motorResponse>maxSpeed):
        motorResponse=maxSpeed
    if(motorResponse<-maxSpeed):
        motorResponse=-maxSpeed
    if(motorResponse>0):
        rightSpeed=maxSpeed
        leftSpeed=maxSpeed-motorResponse
    else:
        rightSpeed=maxSpeed+motorResponse
        leftSpeed=maxSpeed
        
def motor(left,right):
    if(right>0):
        GPIO.output(motorpin1A,GPIO.HIGH)
        GPIO.output(motorpin2A,GPIO.LOW)
        pwmA.ChangeDutyCycle(right)
    else:
        GPIO.output(motorpin1A,GPIO.LOW)
        GPIO.output(motorpin2A,GPIO.HIGH)
        pwmA.ChangeDutyCycle(-right)
        
    if(left>0):
        GPIO.output(motorpin1B,GPIO.HIGH)
        GPIO.output(motorpin2B,GPIO.LOW)
        pwmB.ChangeDutyCycle(left)
    else:
        GPIO.output(motorpin1B,GPIO.LOW)
        GPIO.output(motorpin2B,GPIO.HIGH)
        pwmB.ChangeDutyCycle(-left)
        
        
def plannedCRotate():
    GPIO.output(motorpin1A,GPIO.LOW)
    GPIO.output(motorpin2A,GPIO.HIGH)
    pwmA.ChangeDutyCycle(50)
    GPIO.output(motorpin1B,GPIO.HIGH)
    GPIO.output(motorpin2B,GPIO.LOW)
    pwmB.ChangeDutyCycle(50)
    

def brake():
    GPIO.output(motorpin1A,GPIO.HIGH)
    GPIO.output(motorpin2A,GPIO.LOW)
    pwmA.ChangeDutyCycle(0)
    GPIO.output(motorpin1B,GPIO.HIGH)
    GPIO.output(motorpin2B,GPIO.LOW)
    pwmB.ChangeDutyCycle(0)
       

#Auto calibration
def calibration():
        plannedCRotate();
        upSum=0
        lowSum=0
        #global blackLimit
        IRread()
        #blackLimit = [0]*sensorNum 
        sensorArray=[[0]*sensorNum,[0]*sensorNum]
        
        for i in range(0,sensorNum):
            sensorArray[0][i] = IR_array[i]
            print("sensor Array [0]")
            print(sensorArray[0][i])
            sensorArray[1][i] = IR_array[i]
            print("sensor Array [1]")
            print(sensorArray[1][i])

        loopCounter = int(time*1000/2.5)

        while loopCounter:
            for i in range(0,sensorNum):
                if(IR_array[i]<sensorArray[0][i]):
                    sensorArray[0][i]=IR_array[i]
                if(IR_array[i]>sensorArray[1][i]):
                    sensorArray[1][i]=IR_array[i]
            loopCounter -= 1
        
        for i in range(0,sensorNum):
            blackLimit[i] = int(sensorArray[0][i] + safety * (sensorArray[1][i] - sensorArray[0][i]))
        
        brake()
        
        

        
def printTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    print("GPU temperature is {}".format(temp[5:]))
     
    
calibration()


try:
    while True:
        sensorMapping()
        print("mappedValue")
        print(mappedValue)
        
        for i in range(0,sensorNum):
            if(IR_array[i]<blackLimit[i]):
                print("IR_array[i]<blackLimit[i]")
        if (stopcounter>contiBlack):
            brake()
            time.sleep(0.5)
        if(mappedValue != 0):
            print("applying pid")
            pid()
            motor(leftSpeed, rightSpeed)
            lastAct = mappedValue
        else:
            if(lastAct<targetValue):
                if(rightSpeed>leftSpeed):
                    motor(leftSpeed, rightSpeed)
                else:
                    motor(rightSpeed, leftSpeed)
            else:
                if(leftSpeed>rightSpeed):
                    motor(leftSpeed, rightSpeed)
                else:
                    motor(rightSpeed, leftSpeed)
        
except KeyboardInterrupt:
    GPIO.cleanup()
    print("")
        
"""def controlLED():
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
controlLED()"""