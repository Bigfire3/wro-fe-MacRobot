#!/usr/bin/env python3

# libraries
from math import sin
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
import felib
from ev3dev2.port import LegoPort
from ev3dev2.button import Button
from time import sleep
import threading

# functions
class Object:
    pid = felib.myPID(0.1, 1, 0, 0)
    def __init__(self, color, sign):
        self.color = color
        self.sign = sign

    def object_action(self, x_pos, height):
        felib.set_leds(self.color)
        if x_pos < 25 and height > 70: # pass
            felib.set_leds("BLACK")
            felib.set_steering(0, block = True)
            drive_motor.on_for_rotations(my_speed, (0.5 + abs(2 * sin(gyro_sensor.angle + felib.rounds * 90))) / 2.9225)
        else:
            if x_pos > 25 and height > 110: # back
                felib.set_steering(-60 * self.sign, block = True)
                drive_motor.on_for_rotations(-my_speed, 2 / 2.9225)
                felib.set_steering(0, block = True)
                drive_motor.on_for_rotations(my_speed, 3 / 2.9225)
            else: # aim
                test_value = -0.4 * x_pos + 75
                if test_value < 0:
                    test_value = 0
                set_value = height
                pid_value = self.pid.run(set_value, test_value)
                calculated_steering = felib.max_range((pid_value) * (2 * self.sign)) * self.sign
                felib.set_steering(calculated_steering * self.sign)

# main
if __name__ == "__main__":
    # motors
    steering_motor = MediumMotor(OUTPUT_A)
    drive_motor = LargeMotor(OUTPUT_B)

    # sensors
    ultrasonic_sensor = UltrasonicSensor(INPUT_2)
    gyro_sensor = GyroSensor(INPUT_3)
    color_sensor = ColorSensor(INPUT_4)
    LegoPort(INPUT_1).mode = "auto"
    sleep(2)
    pixy_cam = Sensor(INPUT_1)
    pixy_cam.mode = "ALL"

    # others
    button = Button()

    # variables
    clockwise = True
    sig_switch = 3
    my_speed = 30
    """
    1-3 = red, true, left
    4-6 = green, false, right

    sig_switch = 4 = green worse
    sig_switch = 5 = red worse
    """
    red_object = Object("RED", 1)
    green_object = Object("GREEN", -1)
    line_thread = threading.Thread(target = felib.round_counter)


    felib.set_leds("BLACK")
    steering_motor.reset()
    sleep(1)
    felib.reset_gyro_sensor()
    line_thread.start()
    button.wait_for_bump("enter")
    sleep(1)
    felib.set_leds("BLACK")

    while (-13 < felib.rounds < 13):
        drive_motor.on(my_speed)
        
        sig = pixy_cam.value(1) * 256 + pixy_cam.value(0) # Signature of largest object
        x_pos = pixy_cam.value(2)    # X-centroid of largest SIG1-object
        #y_pos = pixy_cam.value(3)    # Y-centroid of largest SIG1-object
        #width = pixy_cam.value(4)         # Width of the largest SIG1-object
        height = pixy_cam.value(5)        # Height of the largest SIG1-object

        if (height > 15):
            if sig > sig_switch:
                x_pos = 255 - x_pos
                steering_point = green_object.object_action(x_pos, height)
            else:
                steering_point = red_object.object_action(x_pos, height)

        else:
            felib.set_leds("BLACK")
            set_point = -2 * (gyro_sensor.angle - (felib.rounds * 90))
            s2_raw = ultrasonic_sensor.distance_centimeters_continuous
            felib.set_steering(felib.max_range(set_point + (15 - s2_raw)))

    drive_motor.off()
    felib.set_steering(0, block = True)
    steering_motor.off()
