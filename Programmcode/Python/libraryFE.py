#!/usr/bin/python3

'''
0: No color
1: Black
2: Blue
3: Green
4: Yellow
5: Red
6: White
7: Brown
'''

from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *

steering_motor = MediumMotor(OUTPUT_A)
color_sensor = ColorSensor(INPUT_3)

def MaxRange(test_value):
    value = test_value
    if (test_value > 100):
        value = 100
    elif (test_value < -100):
        value = -100
    return value

def WaitForColor(color):
    while (color_sensor.color != color):
        pass

def SetSteering(direction):
    pid = myPID(0.1, 1, 0, 0)
    while(not ((steering_motor.degrees > direction - 3) and (steering_motor.degrees < direction + 3))):
        test_point = steering_motor.degrees
        set_point = direction
        pid_speed = pid.run(set_point, test_point)
        steering_motor.on(MaxRange(pid_speed))
    steering_motor.off()

class myPID :
    dt  = 0.0
    kp  = 0.0
    kd  = 0.0
    ki  = 0.0
    err = 0.0
    int = 0.0
    def __init__(self, dt, kp, kd, ki):
        self.dt  = dt
        self.kp  = kp
        self.kd  = kd
        self.ki  = ki

    def run(self, set, act):
        error = set - act

        P = self.kp * error

        self.int += error * self.dt
        I = self.ki * self.int

        D = self.kd * (error - self.err) / self.dt

        output = P + I + D

        self.err = error
        return(output)