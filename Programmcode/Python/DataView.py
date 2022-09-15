#!/usr/bin/env python3

from time import sleep
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *

steering_motor = MediumMotor(OUTPUT_A)
drive_motor = MediumMotor(OUTPUT_B)
#gyro_sensor = GyroSensor(INPUT_2)
#color_sensor = ColorSensor(INPUT_3)
#ultrasonic_sensor = UltrasonicSensor(INPUT_1)
#infrared_sensor = InfraredSensor(INPUT_4)

while (True):
    # display degrees
    print(steering_motor.degrees, file = sys.stderr) # , to write something in VS Code output)
    sleep(0.1)
    