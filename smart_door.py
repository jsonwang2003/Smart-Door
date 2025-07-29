import board
from digitalio import DigitalInOut, Direction, Pull
import pwmio
from adafruit_motor import servo
import time
import usb_cdc

# Setting up the servo
# angles = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180]
# opp_angles = [180, 160, 140, 120, 100, 80, 60, 40, 20, 0]
pwm = pwmio.PWMOut(board.D5, duty_cycle= 2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

# Save the current time to check for timeouts
# Default timeout is 5 seconds -> if no face is recognized for 5 seconds, the servo will lock the door
startTime = time.monotonic()

# Access the default USB serial port
uart = usb_cdc.console

# Initialize the servo to the starting position
my_servo.angle = 0

while True:
    # Check if there is data available from the USB serial port
    if uart.in_waiting > 0:
        data = uart.readline().decode('utf-8').strip()

        # Check the received data and control the servo accordingly
        if data == "True":
            # The user is recognized
            my_servo.angle = 180
            print("Match")
            startTime = time.monotonic()
        else:
            # The user is not recognized or no face is detected
            print("No match")
            if time.monotonic() - startTime > 5:
                my_servo.angle = 0
                print(time.monotonic() - startTime)
                print("Time out")

    time.sleep(1)