"""
right_motor.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
Controls the right motor using PWM and direction signals. 
Includes functionality for enabling, disabling, and updating 
the motor speed with a duty cycle adjustment based on a constant multiplier.

Functionality:
- Enables and disables the right motor driver.
- Adjusts motor effort based on the commanded duty cycle.
- Applies a battery voltage compensation factor to maintain consistent performance.
- Ensures duty cycle remains within the valid range (-100 to 100).
- Runs as a task in the scheduler to continuously update motor speed.
"""

import init
from pyb import Pin, Timer

class Right_Motor:
    def __init__(self, PWM, DIR, nSLP, timer_num, channel):
        # Initializes the right motor with PWM, direction, and sleep control.
        self.DIR_pin = Pin(DIR, mode=Pin.OUT_PP, value=0)
        self.nSLP_pin = Pin(nSLP, mode=Pin.OUT_PP, value=0)
        self.timer = Timer(timer_num, freq=20000)
        self.PWM = self.timer.channel(channel, Timer.PWM, pin=Pin(PWM))

    def enable(self):
        # Enables the motor driver.
        self.nSLP_pin.value(1)

    def disable(self):
        # Disables the motor driver.
        self.nSLP_pin.value(0)

    def update(self, duty_cycle):
        # Updates the motor speed with a duty cycle compensation.

        # Retrieve the constant multiplier for battery voltage compensation
        multiplier = init.constant_multiplier.get()

        # Apply the multiplier and clamp the value to -100 to 100
        compensated_duty = max(-100, min(100, duty_cycle * multiplier))

        # Set the motor direction and apply the compensated duty cycle
        if compensated_duty < 0:
            self.DIR_pin.high()
            self.PWM.pulse_width_percent(abs(compensated_duty))
        else:
            self.DIR_pin.low()
            self.PWM.pulse_width_percent(compensated_duty)

# Instance of the right motor
right_motor = Right_Motor(
    PWM='PB7',
    DIR='PC10',
    nSLP='PC11',
    timer_num=4,
    channel=2
)

def task_right_motor():
    # Continuously updates the right motor effort based on control input.

    while True:
        duty_cycle_r = init.right_effort.get()
        right_motor.update(duty_cycle_r)
        yield 0
