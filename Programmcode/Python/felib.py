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
gyro_sensor = GyroSensor(INPUT_3)
color_sensor = ColorSensor(INPUT_4)

# others
lcd = Display()
leds = Leds()

# variables
clockwise = False
rounds = 0


def show_text(string, font_name = "courB24", font_width = 15, font_height = 24):
    lcd.clear()
    strings = wrap(string, width = int(180 / font_width))
    for i in range(len(strings)):
        x_val = 89 - font_width / 2 * len(strings[i])
        y_val = 63 - (font_height + 1) * (len(strings) / 2 - i)
        lcd.text_pixels(strings[i], False, x_val, y_val, font=font_name)
    lcd.update()

def max_range(value, min = -100, max = 100):
    if (value < min):
        return min
    elif (value > max):
        return max
    else:
        return value

def wait_for_color(color):
    while (color_sensor.color != color):
        pass

def set_steering(direction, block = True):
    pid = myPID(0.1, 1, 0, 0)
    if block:
        while(not (direction - 3 < -steering_motor.degrees < direction + 3)):
            test_value = -steering_motor.degrees
            set_value = direction
            pid_speed = pid.run(set_value, test_value)
            steering_motor.on(-max_range(pid_speed))
        steering_motor.off()
    else:
        test_value = -steering_motor.degrees
        set_value = direction
        pid_speed = pid.run(set_value, test_value)
        steering_motor.on(-max_range(pid_speed))

def set_leds(color):
    leds.set_color("LEFT", color)
    leds.set_color("RIGHT", color)

def reset_gyro_sensor():
    set_leds("RED")
    '''
        while (gyro_sensor.angle == gyro_sensor.angle):
        LegoPort(INPUT_2).mode = "auto" # change port mode
        gyro_sensor = GyroSensor(INPUT_2)
    '''
    set_leds("YELLOW")
    while (not (gyro_sensor.angle == gyro_sensor.angle)):
        pass
    sleep(1)
    gyro_sensor.reset()
    sleep(1)
    set_leds("GREEN")

def round_counter():
    global rounds
    while -13 < rounds < 13:
        if color_sensor.color == 5: # red/orange
            if rounds == 0:
                clockwise = True
            if clockwise:
                rounds += 1
                wait_for_color(6)
            print(rounds, file = sys.stderr)
              
        elif color_sensor.color == 2 or color_sensor.color == 0: # blue
            if rounds == 0:
                clockwise = False
            if not clockwise:
                rounds -= 1
                wait_for_color(6)

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