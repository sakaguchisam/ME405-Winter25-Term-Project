"""
init.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
Defines shared variables and queues for inter-task communication.
These include encoder data, motor efforts, state control, and 
sensor readings used in the robot's operation.
"""

import task_share
from task_share import Share, Queue
import cqueue
from pyb import Pin, Timer

# Shared variable for current encoder value
current_encoder_left = Share('f', thread_protect=True, name="Current Encoder Left")
current_encoder_left.put(0)

# Queue for bump events
bump_flag = Queue('b', 1, thread_protect=True, name="Bump Flag")

# Shared variables for robot control
distance_share = Share('f', thread_protect=True, name="Distance Share")
left_effort = Share('h', thread_protect=True, name="Left Motor Effort")
right_effort = Share('h', thread_protect=True, name="Right Motor Effort")
state_input = Share('h', thread_protect=True, name="State Input")

# Queues for data collection
collection_data_queue = Queue('f', 100, thread_protect=True, name="Collection Queue")
init_heading = Share('f', thread_protect=True, name="Init Heading")

# Data collection flag (active/inactive)
data_collection_active = Share('b', thread_protect=True, name="Data Collection Active")
data_collection_active.put(0)

# Robot mode: 0 for normal, 1 for go-straight override
robot_mode = Share('h', thread_protect=True, name="Robot Mode")
robot_mode.put(0)

# Cumulative encoder distance
cumulative_distance = Share('f', thread_protect=True, name="Cumulative Distance")
cumulative_distance.put(0.0)

# Queues for encoder data storage
queue_size = 600
encoder_left_data_queue = Queue('f', queue_size, thread_protect=True, name="Encoder Left Data Queue")
encoder_right_data_queue = Queue('f', queue_size, thread_protect=True, name="Encoder Right Data Queue")

# Flag to control line sensing (PID control)
line_sensing_enabled = Share('b', thread_protect=True, name="Line Sensing Enabled")
line_sensing_enabled.put(1)  # 1 = enabled, 0 = disabled

# Override mode flag: 0 = normal (PID active), 1 = override active
override_mode = Share('b', thread_protect=True, name="Override Mode")
override_mode.put(0)

# Battery-related shared variables
battery_voltage = Share('f', thread_protect=False, name="battery_voltage")
constant_multiplier = Share('f', thread_protect=False, name="constant_multiplier")

# PID control proportional gain value
kp_value = Share('f', thread_protect=True, name="kp_value")
kp_value.put(0.5)

# Final sequence control flag
final_flag = Share('b', thread_protect=True, name="Final Flag")
final_flag.put(0)

# Queue for final target values
final_target_queue = Queue('f', 1, thread_protect=True, name="Final Target Queue")
