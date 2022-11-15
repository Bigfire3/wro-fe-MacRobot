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
from ev3dev2.led import Leds
import time

# motors
steering_motor = MediumMotor(OUTPUT_A)

# sensors
gyro_sensor = GyroSensor(INPUT_3)
color_sensor = ColorSensor(INPUT_4)

# others
leds = Leds()

# variables
clockwise = False
rounds = 0

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

def set_steering(direction, block = False):
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
    time.sleep(1)
    gyro_sensor.reset()
    time.sleep(1)
    set_leds("GREEN")

def round_counter():
    global rounds
    color_sensor.calibrate_white()
    time.sleep(1)
    d_times = []
    old_time = 0
    while -12 < rounds < 12:
        if color_sensor.color == 5: # red/orange
            if rounds == 0:
                clockwise = True
            if clockwise:
                rounds += 1
                wait_for_color(6)
                if old_time == 0:
                    old_time = time.time()
                else:
                    d_times.append(time.time() - old_time)
                    old_time = time.time()
              
        elif color_sensor.color == 2: # blue
            if rounds == 0:
                clockwise = False
            if not clockwise:
                rounds -= 1
                wait_for_color(6)
                if old_time == 0:
                    old_time = time.time()
                else:
                    d_times.append(time.time() - old_time)
                    old_time = time.time()
    
    sum = 0
    num = 0
    for value in d_times:
        sum += value
        num += 1
    time_to_sleep = (sum / num) / 2
    print(time_to_sleep)
    time.sleep(time_to_sleep)

    if clockwise:
        rounds += 1
    else:
        rounds -= 1

class myPID:
    dt  = 0.0
    kp  = 0.0
    kd  = 0.0
    ki  = 0.0
    err = 0.0
    int = 0.0
    def __init__(self, dt, kp, ki, kd):
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
        