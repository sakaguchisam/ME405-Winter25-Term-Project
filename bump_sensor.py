"""
bump_sensor.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
Sets up external interrupts for four bump sensors (pull-up, falling edge)
and provides a cooperative task to react to bump_flag. 

Functionality:
- Initializes bump sensors as external interrupts.
- Uses a minimal ISR to set a bump_flag when a sensor is triggered.
- Implements a cooperative task to handle bump events and execute navigation maneuvers.
- Provides a wall navigation function to move and turn the robot based on pre-set timing.
"""

from pyb import Pin, ExtInt
import micropython
import init
from left_motor import left_motor
from right_motor import right_motor
from time import ticks_ms, ticks_diff

micropython.alloc_emergency_exception_buf(100)  # Helps avoid MemoryError in ISR

# ---------------------------------------------------------------------
# 1) Interrupt Callback for Bump Sensors
# ---------------------------------------------------------------------
def bump_callback(line):
    # Sets the bump flag when any bump sensor is triggered.
    init.bump_flag = True

# ---------------------------------------------------------------------
# 2) Initialize Bump Sensors (Interrupts)
# ---------------------------------------------------------------------
def init_bump_sensors():
    # Configures bump sensors with pull-up resistors and falling-edge interrupts.

    sensor_map = {
        1: 'PB5',  # EXTI5
        2: 'PB3',  # EXTI3
        3: 'PB6',  # EXTI6
        4: 'PA7',  # EXTI7
    }

    for sensor_idx, pin_name in sensor_map.items():
        pin_obj = Pin(pin_name, Pin.IN, Pin.PULL_UP)
        ExtInt(pin_obj, ExtInt.IRQ_FALLING, Pin.PULL_UP, bump_callback)

    print("Bump sensors initialized with pull-up & falling-edge interrupts.")

# ---------------------------------------------------------------------
# 3) Wall Navigation Function
# ---------------------------------------------------------------------
def wall_nav(left_pwm, right_pwm, duration):
    # Moves the robot for a set duration using specified PWM values.

    left_motor.update(left_pwm)
    right_motor.update(right_pwm)
    start_time = ticks_ms()
    
    while ticks_diff(ticks_ms(), start_time) < duration:
        pass  # Wait for the specified duration
    
    left_motor.update(0)
    right_motor.update(0)

# ---------------------------------------------------------------------
# 4) Task to Handle Bump Events
# ---------------------------------------------------------------------
def task_bump_handling():
    """
    Cooperative task that checks for bump events.
    If a bump is detected, executes a navigation sequence to maneuver the robot.
    """
    while True:
        if init.bump_flag:
            # Reverse
            wall_nav(-20, -20, 400)  # Reverse for 400ms
            # Turn 90 degrees right
            wall_nav(20, -20, 600)  # Turn right
            # Move forward
            wall_nav(20, 20, 600)  # Move forward
            # Turn -90 degrees left
            wall_nav(-20, 20, 400)  # Turn left
            # Move forward
            wall_nav(20, 20, 300)  # Move forward
            # Turn -90 degre
