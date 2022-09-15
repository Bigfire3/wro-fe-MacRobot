#!/usr/bin/env python3

from math import sin
from time import sleep
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
import libraryFE
from ev3dev2.port import LegoPort


steering_motor = MediumMotor(OUTPUT_A)
drive_motor = MediumMotor(OUTPUT_B)
gyro_sensor = GyroSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_3)

LegoPort(INPUT_4).mode = "auto"
sleep(2)
pixy_cam = Sensor(INPUT_4)
pixy_cam.mode = "ALL"

pid = libraryFE.myPID(0.1, 2, 0, 1)
pid_aim_object = libraryFE.myPID(0.1, 1, 0, 0.5)

rounds = 0
clockwise = True
rotation = 0

def pass_object(sig):
    global pid_aim_object
    global x_centroid
    global height
    if (sig == 1):
        direction = 1
        shift = 60
    else:
        direction = -1
        shift = 210

    if ((sig == 1 and x_centroid > 240 and height > 70) or (sig == 2 and x_centroid < 13 and height > 70)): # drive around
        libraryFE.SetSteering(0)
        drive_motor.on_for_rotations(50, 1.5 + abs(2 * sin(gyro_sensor.angle + rounds * 90)))
    else:
        if (height > 120):
            libraryFE.SetSteering(60 * direction)
            drive_motor.on_for_rotations(-50, 2)
            libraryFE.SetSteering(0)
            drive_motor.on_for_rotations(50, 3)
        else:
            test_point = steering_motor.degrees
            set_point = (height * (64/25 * direction) + shift) - x_centroid
            # print(set_point, file = sys.stderr)
            pid_speed = pid_aim_object.run(set_point, test_point)
            steering_motor.on(libraryFE.MaxRange(pid_speed))

# main
steering_motor.reset()
gyro_sensor.reset()

while (rounds < 13 or rounds > -13):
    if (color_sensor.MODE_COL_COLOR == 5):
        if (rounds == 0):
            clockwise = True
        if (clockwise == True):
            rounds += 1
            libraryFE.WaitForColor(6)
    elif (color_sensor.MODE_COL_COLOR == 2):
        if (rounds == 0):
            clockwise = False
        if (clockwise == False):
            rounds -= 1
            libraryFE.WaitForColor(6)
    
    sig = pixy_cam.value(1) * 256 + pixy_cam.value(0) # Signature of largest object
    x_centroid = pixy_cam.value(2)    # X-centroid of largest SIG1-object
    #y_centroid = pixy_cam.value(3)    # Y-centroid of largest SIG1-object
    #width = pixy_cam.value(4)         # Width of the largest SIG1-object
    height = pixy_cam.value(5)        # Height of the largest SIG1-object

    if (height > 25):
        drive_motor.on(50)
        if (sig == 0):
            steering_motor.off()
        elif (sig == 1):
            pass_object(1)
        elif (sig == 2):
            pass_object(2)

    else:
        drive_motor.on(50)
        test_point = steering_motor.degrees
        set_point = libraryFE.MaxRange((gyro_sensor.angle - (rounds * 90)) * 4)
        pid_speed = pid.run(set_point, test_point)
        steering_motor.on(libraryFE.MaxRange(pid_speed))


libraryFE.SetSteering(0)
steering_motor.off()
drive_motor.on_for_rotations(-50, 7)
