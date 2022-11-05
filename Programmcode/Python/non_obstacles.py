#!/usr/bin/env python3

# libraries
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2._platform.ev3 import *
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

    # variables
    sign = 0

    # main
    steering_motor.reset()
    felib.reset_gyro_sensor()
    line_thread = threading.Thread(target = felib.round_counter)
    line_thread.start()

    while -12 < felib.rounds < 12:
        drive_motor.on(100)
        s1_raw = ultrasonic_sensor1.distance_centimeters_continuous
        sign = felib.rounds / abs(felib.rounds) if felib.rounds != 0 else 0
        if sign == 0:
            sign1 = 1
        else:
            sign1 = sign

        if sign > 0:
            felib.set_leds("RED")
        elif sign < 0:
            felib.set_leds("GREEN")
        else:
            felib.set_leds("BLACK")
        value = -s1_raw + 100
        if value < 0 or sign == 0:
            set_point = -2 * (gyro_sensor.angle - (felib.rounds * 90))
            s2_raw = ultrasonic_sensor2.distance_centimeters_continuous
            if s2_raw < 20:
                set_point += (20 - s2_raw) * 2
            if s2_raw > 30:
                set_point -= (s2_raw - 30) * 2
            felib.set_steering(felib.max_range(sign1 * set_point), block = False)
        else:
            felib.set_steering(felib.max_range(sign * value), block = False)
            
    drive_motor.off()
    felib.set_steering(0)