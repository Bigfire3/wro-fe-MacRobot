#!/usr/bin/env python3

# libraries
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
from ev3dev2.button import Button
import felib
import threading

if __name__ == "__main__":
    # motors
    steering_motor = MediumMotor(OUTPUT_A)
    drive_motor = LargeMotor(OUTPUT_B)

    # sensors
    ultrasonic_sensor1 = UltrasonicSensor(INPUT_1)
    ultrasonic_sensor2 = UltrasonicSensor(INPUT_2)
    gyro_sensor = GyroSensor(INPUT_3)

    # others
    button = Button()

    # variables
    sign = 0
    old_s1 = 0

    # main
    felib.set_leds("ORANGE")
    button.wait_for_bump("enter")
    steering_motor.reset()
    felib.reset_gyro_sensor()
    line_thread = threading.Thread(target = felib.round_counter)
    line_thread.start()

    while -13 < felib.rounds < 13:
        s1_raw = ultrasonic_sensor1.distance_centimeters_continuous
        d_s1 = old_s1 - s1_raw
        if not(-10 < d_s1 < 10):
            old_s1 = s1_raw
            s1_raw = 101
        old_s1 = s1_raw
        
        if (0 < d_s1 < 20) and (s1_raw < 120):
            drive_motor.on(35)
        else:
            drive_motor.on(100)

        if felib.rounds != 0:
            sign = felib.rounds / abs(felib.rounds)
        else:
            sign = 0

        value = -s1_raw + 100
        if value < 0 or sign == 0:
            set_point = -2 * (gyro_sensor.angle - (felib.rounds * 90))
            s2_raw = ultrasonic_sensor2.distance_centimeters_continuous
            if felib.rounds >= 0:
                threshold = 15
            else:
                threshold = 20
            mutliplier = 1.5 if s2_raw > threshold else 3
            set_point = set_point + ((threshold - s2_raw) * mutliplier)
            felib.set_steering(felib.max_range(set_point))
        else:
            felib.set_steering(felib.max_range(sign * value))
            
    drive_motor.off()
    felib.set_steering(0, block = True)