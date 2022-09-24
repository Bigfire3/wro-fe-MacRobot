#!/usr/bin/env python3

# libraries
from math import sin
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
import libraryFE
from ev3dev2.port import LegoPort
from ev3dev2.button import Button
from time import sleep

# motors
steering_motor = MediumMotor(OUTPUT_A)
drive_motor = MediumMotor(OUTPUT_B)

# sensors
gyro_sensor = GyroSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_3)
LegoPort(INPUT_4).mode = "auto"
sleep(2)
pixy_cam = Sensor(INPUT_4)
pixy_cam.mode = "ALL"

# others
button = Button()

# variables
pid = libraryFE.myPID(0.1, 2, 0, 0)
rounds = 0
clockwise = True
rotation = 0

# functions
def pass_object(sig, x_pos, height):
    global pid
    """
    1-3 = red, true, left
    4-6 = green, false, right

    sig_switch = 4 = green worse
    sig_switch = 5 = red worse
    """
    sig_switch = 4
    if (sig < sig_switch):
        libraryFE.SetLeds("RED")
        target_x_pos = 25
        back_x_pos = 20
        sign = 1
        n = 75.97
    else:
        libraryFE.SetLeds("GREEN")
        target_x_pos = 230
        back_x_pos = 235
        sign = -1
        n = -26.43

    if (((sig < sig_switch and x_pos < target_x_pos) or (sig > sig_switch and x_pos > target_x_pos)) and height > 70): # pass
        libraryFE.SetLeds("BLACK")
        libraryFE.SetSteering(0)
        drive_motor.on_for_rotations(50, 1.5 + abs(2 * sin(gyro_sensor.angle + rounds * 90)))
    else:
        if (((sig < sig_switch and x_pos > back_x_pos) or (sig > sig_switch and x_pos < back_x_pos)) and height > 110): # back
            libraryFE.SetSteering(-60 * sign)
            drive_motor.on_for_rotations(-50, 2)
            libraryFE.SetSteering(0)
            drive_motor.on_for_rotations(50, 3)
        else: # aim
            test_value = (-0.4 * sign) * x_pos + n
            set_value = height
            pid_value = pid.run(set_value, test_value)
            libraryFE.SetSteering(libraryFE.MaxRange(pid_value) * (2 * sign))

# main
if (__name__ == "__main__"):
    libraryFE.SetLeds("BLACK")
    steering_motor.reset()
    libraryFE.ResetGyroSensor()
    button.wait_for_bump("enter")
    sleep(1)
    libraryFE.SetLeds("BLACK")

    while (-13 < rounds < 13):
        drive_motor.on(50)
        if (color_sensor.MODE_COL_COLOR == 5): # red/orange
            if (rounds == 0):
                clockwise = True
            if (clockwise):
                rounds += 1
                libraryFE.WaitForColor(6)
        elif (color_sensor.MODE_COL_COLOR == 2): # blue
            if (rounds == 0):
                clockwise = False
            if (not clockwise):
                rounds -= 1
                libraryFE.WaitForColor(6)
        
        sig = pixy_cam.value(1) * 256 + pixy_cam.value(0) # Signature of largest object
        x_pos = pixy_cam.value(2)    # X-centroid of largest SIG1-object
        #y_pos = pixy_cam.value(3)    # Y-centroid of largest SIG1-object
        #width = pixy_cam.value(4)         # Width of the largest SIG1-object
        height = pixy_cam.value(5)        # Height of the largest SIG1-object

        if (height > 25):
            pass_object(sig, x_pos, height)

        else:
            libraryFE.SetLeds("BLACK")
            drive_motor.on(50)
            steering_motor.on(-libraryFE.MaxRange((gyro_sensor.angle - rounds * 90) * 3))

    drive_motor.off()
    libraryFE.SetSteering(0)
    steering_motor.off()
