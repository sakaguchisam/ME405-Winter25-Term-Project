"""
task_encoder.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
Handles encoder data collection for position, velocity, and timing. 
Encoders are zeroed when data collection starts and updated continuously 
until data collection is complete.

Functionality:
- Initializes left and right encoders.
- Zeroes encoders at the start of data collection to ensure accurate readings.
- Updates position, velocity, and elapsed time for both encoders.
- Stores encoder data in a queue for later processing.
- Stops data collection when the queue is full.
"""

import init
import time
from encoder import Encoder
from time import sleep_us

# Initialize encoders for left and right motors
left_enc = Encoder(
    tim=1,
    chA_pin='PA9',
    chB_pin='PA8'
)

right_enc = Encoder(
    tim=8,
    chA_pin='PC7',
    chB_pin='PC6'
)

def task_encoder():
    # Collects encoder data while data collection is active.

    zeroed = False  # Ensures encoders are zeroed only once per session

    while True:
        # Reset flag when data collection is inactive
        if init.data_collection_active.get() == 0:
            zeroed = False
            yield 0
            continue

        # Zero the encoders at the start of data collection
        if not zeroed:
            left_enc.zero()
            right_enc.zero()
            zeroed = True

        # Update encoder counts and timing
        left_enc.update()
        right_enc.update()

        l_pos = left_enc.get_position()
        r_pos = right_enc.get_position()
        l_vel = left_enc.get_velocity()
        r_vel = right_enc.get_velocity()
        l_time = left_enc.get_time()
        r_time = right_enc.get_time()

        # Store data in the queue if space is available
        if not init.encoder_data_queue.full():
            init.encoder_data_queue.put(l_time)
            init.encoder_data_queue.put(l_pos)
            init.encoder_data_queue.put(l_vel)
            init.encoder_data_queue.put(r_time)
            init.encoder_data_queue.put(r_pos)
            init.encoder_data_queue.put(r_vel)
        else:
            print("Data Collection complete")
            zeroed = False
            init.data_collection_active.put(0)  # Deactivate data collection
            yield 0

        sleep_us(100)  # Prevents excessive CPU usage
        yield 0
