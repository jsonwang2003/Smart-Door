import board

from digitalio import DigitalInOut, Direction, Pull

import pwmio

from adafruit_motor import servo

import time

import usb_cdc

pwm = pwmio.PWMOut(board.D5, duty_cycle= 2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

startTime = time.monotonic()

# angles = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]
# opp_angles = [180, 160, 140, 120, 100, 80, 60, 40, 20, 0]

# Access the default USB serial port
uart = usb_cdc.console

my_servo.angle = 0

while True:

    # Read data from the computer
    if uart.in_waiting > 0:
        data = uart.readline().decode('utf-8').strip()
        if data == "True":
            my_servo.angle = 180
            print("Match")
            startTime = time.monotonic()
        elif data == "False":
            print("No match")
            if time.monotonic() - startTime > 5:
                my_servo.angle = 0
                print(time.monotonic() - startTime)
                print("Time out")
        elif data == "No face":
            print("No face")
            if time.monotonic() - startTime > 5:
                my_servo.angle = 0
                print(time.monotonic() - startTime)
                print("Time out")

    time.sleep(1)