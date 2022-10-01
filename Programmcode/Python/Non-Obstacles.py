#!/usr/bin/env python3

# libraries
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
import lib

# motors
steering_motor = MediumMotor(OUTPUT_A)
drive_motor = MediumMotor(OUTPUT_B)

# sensors
# ultrasonic_sensor = UltrasonicSensor(INPUT_1)
gyro_sensor = GyroSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_3)
ultrasonic_sensor = UltrasonicSensor(INPUT_4)

# variables
rounds = 0
rotation = 0
clockwise = True

# main
steering_motor.reset()
gyro_sensor.reset()
drive_motor.on(50)

pid = lib.myPID(0.1, 1, 0, 1)

while (-13 < rounds < 13):
    #print(color_sensor.color, file = sys.stderr)
    if (color_sensor.color == 5):
        if(rounds == 0):
            clockwise = True
        if(clockwise == True):
            rounds += 1
            lib.WaitForColor(6)
    elif(color_sensor.color == 2):
        if(rounds == 0):
            clockwise = False
        if(clockwise == False):
            rounds -= 1
            lib.WaitForColor(6)
    
    rotation = gyro_sensor.angle
    gyro_point = rotation - (rounds * 90)
    ultrasonic_point = 25 - ultrasonic_sensor.distance_centimeters
    lib.SetSteering(lib.MaxRange(3 * gyro_point))
    
steering_motor.off()
drive_motor.on_for_rotations(-50, 7)
