"""
encoder.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
This module implements an encoder class for tracking position and velocity.
It utilizes a hardware timer in encoder mode to count pulses from a quadrature
encoder, allowing for real-time position and velocity calculations.
"""

from time import ticks_us, ticks_diff  # Functions for microsecond timing
from pyb import Timer, Pin

class Encoder:
    """Class for handling a quadrature encoder using a hardware timer."""

    def __init__(self, tim, chA_pin, chB_pin):
        # Initializes the encoder using a specified timer and pins.
        # tim: Timer number for the encoder
        # chA_pin: Pin for Channel A
        # chB_pin: Pin for Channel B

        # Configure the timer in encoder mode
        self.enc_timer = Timer(tim, prescaler=0, period=0xFFFF)
        self.chA_PIN = self.enc_timer.channel(1, Timer.ENC_AB, pin=Pin(chA_pin))
        self.chB_PIN = self.enc_timer.channel(2, Timer.ENC_AB, pin=Pin(chB_pin))

        # Encoder count and position tracking
        self.position = 0      # Total accumulated counts
        self.prev_count = 0    # Last recorded count
        self.delta = 0         # Change in count per update
        self.dt = 0            # Time interval between updates (µs)
        self.current_count = 0 # Most recent counter value
        self.AR = 65535        # Timer Auto Reload value (16-bit counter)

        # Time tracking variables
        self.start_time = None   # Timestamp when movement first starts
        self.last_time = ticks_us()  # Last recorded update time

    def update(self):
        # Updates the encoder count, position, and velocity calculations.
        # Corrects for overflow/underflow of the 16-bit counter.

        # Update encoder counts
        self.current_count = self.enc_timer.counter()
        self.delta = self.current_count - self.prev_count
        self.prev_count = self.current_count

        # Correct for counter overflow/underflow
        if self.delta > (self.AR + 1) // 2:
            self.delta -= (self.AR + 1)
        elif self.delta < -((self.AR + 1) // 2):
            self.delta += (self.AR + 1)
        self.position += self.delta

        # Detect movement and set start time if not already set
        if self.start_time is None and abs(self.delta) > 0:
            self.start_time = ticks_us()

        # Update timing calculations
        current_time = ticks_us()
        self.dt = ticks_diff(current_time, self.last_time)
        self.last_time = current_time

    def get_position(self):
        # Returns the encoder position in radians.
        return self.position * 2 * 3.141592653589793 / 1440

    def get_velocity(self):
        # Returns the encoder velocity in radians per second.
        if self.dt == 0:
            return 0
        return (self.delta * 2 * 3.141592653589793 / 1440) / (self.dt / 1_000_000)

    def get_time(self):
        # Returns the elapsed time in seconds since movement started.
        if self.start_time is None:
            return 0  # If no movement has started, return 0
        elapsed = ticks_diff(ticks_us(), self.start_time)
        return elapsed / 1_000_000

    def zero(self):
        # Resets the encoder’s position and time references.
        self.position = 0
        self.dt = 0
        self.start_time = None  # Reset start time when zeroing the encoder
