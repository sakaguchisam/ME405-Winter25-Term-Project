"""
PID_controller.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
Implements a PID controller for line-following. The controller adjusts 
motor efforts based on line sensor error to maintain alignment.

Functionality:
- Uses a proportional-integral-derivative (PID) algorithm to correct the robot's trajectory.
- Reads the latest line sensor error from a queue and computes the required adjustments.
- Adjusts motor effort while ensuring effort values remain within valid bounds.
- If override mode is active, the robot drives straight.
- If grid mode is active, PID corrections are skipped.
"""

import init
import pyb
from time import ticks_us, ticks_diff

# PID Gains
Kp = 10  # Proportional gain
Ki = 0   # Integral gain
Kd = 0.9 # Derivative gain
init.kp_value.put(Kp)

def PID_value():
    # Executes the PID control loop for adjusting motor effort.

    integral = 0.0
    prev_error = 0.0
    prev_time = ticks_us()
    base_speed = 18  # Motor base speed (PWM %)

    while True:
        # Skip PID processing if grid mode is active
        if init.state_input.get() == 1:
            yield 0
            continue

        # Retrieve error value or set default if queue is empty
        error = 0.0
        if not init.collection_data_queue.empty():
            error = init.collection_data_queue.get()

        # Override mode forces straight driving by setting error to zero
        if init.override_mode.get() == 1:
            error = 0.0

        if error == 0:
            integral = 0.0
            prev_error = 0.0
            left_out = base_speed
            right_out = base_speed
        else:
            now = ticks_us()
            dt = ticks_diff(now, prev_time) / 1_000_000.0
            prev_time = now

            p_term = Kp * error
            integral += error * dt
            i_term = Ki * integral
            d_term = 0.0
            if dt > 0:
                d_term = Kd * (error - prev_error) / dt
            prev_error = error

            pid_output = p_term + i_term + d_term

            left_out = base_speed - pid_output
            right_out = base_speed + pid_output

        # Clamp motor efforts to valid range (-100 to 100)
        left_out = max(-100, min(100, left_out))
        right_out = max(-100, min(100, right_out))

        # Update motor effort shares
        init.left_effort.put(int(left_out))
        init.right_effort.put(int(right_out))
        yield 0
