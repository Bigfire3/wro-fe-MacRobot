#!/usr/bin/env python3

# libraries
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
import felib

# motors
steering_motor = MediumMotor(OUTPUT_A)
drive_motor = MediumMotor(OUTPUT_B)

# sensors
# ultrasonic_sensor = UltrasonicSensor(INPUT_1)
gyro_sensor = GyroSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_3)
ultrasonic_sensor = UltrasonicSensor(INPUT_4)

# variables
rotation = 0
clockwise = True

# main
steering_motor.reset()
gyro_sensor.reset()
drive_motor.on(50)

pid = felib.myPID(0.1, 1, 0, 1)

while (-13 < felib.rounds < 13):
    #print(color_sensor.color, file = sys.stderr)
    
    rotation = gyro_sensor.angle
    gyro_point = rotation - (felib.rounds * 90)
    ultrasonic_point = 25 - ultrasonic_sensor.distance_centimeters
    felib.set_steering(felib.max_range(3 * gyro_point))
    
steering_motor.off()
drive_motor.on_for_rotations(-50, 7)
