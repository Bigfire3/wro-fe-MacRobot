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
    color_sensor = ColorSensor(INPUT_4)

    # variables
    offset = 0

    # main
    steering_motor.reset()
    felib.reset_gyro_sensor()
    line_thread = threading.Thread(target = felib.round_counter)
    line_thread.start()

    while -12 < felib.rounds < 12:
        drive_motor.on(0)

        raw_value = ultrasonic_sensor1.distance_centimeters_continuous
        value = -raw_value + 100
        if value < 0:
            set_point = gyro_sensor.angle - (felib.rounds * 90)
            value = ultrasonic_sensor2.distance_centimeters_continuous
            if value < 20:
                set_point -= (20 - value) * 3
            if value > 30:
                set_point += (20 - value) * 3
            felib.set_steering(felib.max_range(-2 * set_point), block = False)
        else:
            felib.set_steering(felib.max_range(-value), block = False)

    drive_motor.off()
    felib.set_steering(0)
