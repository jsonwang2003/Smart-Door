import board

from digitalio import DigitalInOut, Direction, Pull

import pwmio

from adafruit_motor import servo

import time

import usb_cdc

from digitalio import DigitalInOut, Direction, Pull

button1 = DigitalInOut(board.D0)
button1.direction = Direction.INPUT
button1.pull = Pull.UP

pwm = pwmio.PWMOut(board.D5, duty_cycle= 2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)


startTime = time.monotonic()

angles = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]
opp_angles = [180, 160, 140, 120, 100, 80, 60, 40, 20, 0]

# Access the default USB serial port
uart = usb_cdc.console

my_servo.angle = 0

unlocked = False

while True:

    buttonState1 = not button1.value

    

    # Read data from the computer
    if uart.in_waiting > 0:
        data = uart.readline().decode('utf-8').strip()
        if data == "True":
            my_servo.angle = 180
            startTime = time.monotonic()
            print("Match", time.monotonic() - startTime)
            
        elif data == "False":
            print("No match", time.monotonic() - startTime)
            if time.monotonic() - startTime > 9:
                # my_servo.angle = 0
                print("Time out", time.monotonic() - startTime)
        elif data == "No face":
            print("No face", time.monotonic() - startTime)
            if time.monotonic() - startTime > 9:
                # my_servo.angle = 0
                print("Time out", time.monotonic() - startTime)
    elif buttonState1 and unlocked == False:
        my_servo.angle = 180
        startTime = time.monotonic()
        print("Manual Unlock", time.monotonic() - startTime)
        time.sleep(0.5)
        unlocked = True
    elif buttonState1 and unlocked:
        my_servo.angle = 0
        startTime = time.monotonic()
        print("Manual Unlock", time.monotonic() - startTime)
        time.sleep(0.5)
        unlocked = False

    # time.sleep(0.1)

