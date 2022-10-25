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
    ultrasonic_sensor3 = UltrasonicSensor(INPUT_3)
    color_sensor = ColorSensor(INPUT_4)

    # variables
    offset = 0

    # main
    steering_motor.reset()
    line_thread = threading.Thread(target = felib.round_counter)
    line_thread.start()
    
    while -13 < felib.rounds < 13:
        drive_motor.on(50)
        
        if felib.rounds > 0:
            offset = (ultrasonic_sensor3.distance_centimeters - 255) / 10
        elif felib.rounds < 0:
            offset = (ultrasonic_sensor3.distance_centimeters - 255) / -10

        value = (ultrasonic_sensor1.distance_centimeters + offset) / (ultrasonic_sensor2.distance_centimeters - offset)
        if value < 1:
            value = -1 / value
        value = value - (value / abs(value))
        felib.set_steering(felib.max_range(value * -20))





'''
rotation = 0
clockwise = True

# main
gyro_sensor.reset()


pid = felib.myPID(0.1, 1, 0, 1)

while (-13 < felib.rounds < 13):
    #print(color_sensor.color, file = sys.stderr)
    
    rotation = gyro_sensor.angle
    gyro_point = rotation - (felib.rounds * 90)
    ultrasonic_point = 25 - ultrasonic_sensor.distance_centimeters
    felib.set_steering(felib.max_range(3 * gyro_point))
    
steering_motor.off()
drive_motor.on_for_rotations(-50, 7)
'''