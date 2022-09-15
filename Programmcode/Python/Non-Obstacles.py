#!/usr/bin/env python3

# libraries
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
import libraryFE

# motors
steering_motor = MediumMotor(OUTPUT_A)
drive_motor = MediumMotor(OUTPUT_B)

# sensors
infrared_sensor = InfraredSensor(INPUT_1)
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

pid = libraryFE.myPID(0.1, 1, 0, 1)

while (rounds <= 13 or rounds >= 13):
    #print(color_sensor.color, file = sys.stderr)
    if (color_sensor.color == 5):
        if(rounds == 0):
            clockwise = True
        if(clockwise == True):
            rounds += 1
            libraryFE.WaitForColor(6)
    elif(color_sensor.color == 2):
        if(rounds == 0):
            clockwise = False
        if(clockwise == False):
            rounds -= 1
            libraryFE.WaitForColor(6)
    
    rotation = gyro_sensor.angle
    if (ultrasonic_sensor.distance_centimeters < 15):
        rotation -= 15
    elif(infrared_sensor.proximity < 10.5):
        rotation += 15

    set_point = 2 * ((rotation) - (rounds * 90))
    test_point = steering_motor.degrees
    pid_steering = pid.run(set_point, test_point)
    if ((steering_motor.degrees > 100 and pid_steering > 0) or (steering_motor.degrees < -100 and pid_steering < 0)): pid_steering = 0
    steering_motor.on(libraryFE.MaxRange(pid_steering))
            
steering_motor.off()
drive_motor.on_for_rotations(-50, 7)
