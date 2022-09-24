#!/usr/bin/python3

"""
0: No color
1: Black
2: Blue
3: Green
4: Yellow
5: Red
6: White
7: Brown
"""

from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
from ev3dev2.display import Display
from ev3dev2.led import Leds
from textwrap import wrap
from time import sleep

# motors
steering_motor = MediumMotor(OUTPUT_A)

# sensors
gyro_sensor = GyroSensor(INPUT_2)
color_sensor = ColorSensor(INPUT_3)

# others
lcd = Display()
leds = Leds()

# variables

def showText(string, font_name = "courB24", font_width = 15, font_height = 24):
    lcd.clear()
    strings = wrap(string, width = int(180 / font_width))
    for i in range(len(strings)):
        x_val = 89 - font_width / 2 * len(strings[i])
        y_val = 63 - (font_height + 1) * (len(strings) / 2 - i)
        lcd.text_pixels(strings[i], False, x_val, y_val, font=font_name)
    lcd.update()

def MaxRange(value, min = -100, max = 100):
    if (value < min):
        return min
    elif (value > max):
        return max
    else:
        return value

def WaitForColor(color):
    while (color_sensor.color != color):
        pass

def SetSteering(direction):
    pid = myPID(0.1, 1, 0, 0)
    while(not (direction - 3 < -steering_motor.degrees < direction + 3)):
        test_value = -steering_motor.degrees
        set_value = direction
        pid_speed = pid.run(set_value, test_value)
        steering_motor.on(-MaxRange(pid_speed))
    steering_motor.off()

def SetLeds(color):
    leds.set_color("LEFT", color)
    leds.set_color("RIGHT", color)

def ResetGyroSensor():
    SetLeds("RED")
    while (gyro_sensor.angle == gyro_sensor.angle):
        InfraredSensor(INPUT_2).proximity # read input 2 as infrared to change port mode
    SetLeds("YELLOW")
    while (not (gyro_sensor.angle == gyro_sensor.angle)):
        pass
    sleep(1)
    gyro_sensor.reset()
    sleep(1)
    SetLeds("GREEN")


class myPID:
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
