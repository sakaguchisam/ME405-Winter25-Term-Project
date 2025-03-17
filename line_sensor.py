"""
line_sensor.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
Implements a line sensor driver using ADC inputs. 
Provides methods for reading raw sensor values, performing calibration, 
computing a weighted centroid for line tracking, and adjusting sensor brightness.
"""

import init
import pyb
from pyb import Pin, ADC
from time import ticks_us, ticks_diff
from array import array
from imu import BNO055

class LineSensorDriver:
    def __init__(self, line_pins, brightness_pin=None, led_pin=None, window_size=10, error_range=(-5, 5)):
        # Initializes line sensors, brightness control, and LED control.

        self.adc_line = [ADC(Pin(pin)) for pin in line_pins]
        self.num_line_sensors = len(self.adc_line)

        self.adc_brightness = ADC(Pin(brightness_pin)) if brightness_pin else None
        self.led_pin = Pin(led_pin, Pin.OUT_PP) if led_pin else None

        if self.led_pin:
            self.led_on()

        # Sensor values and brightness tracking
        self.line_values = array('H', [0] * self.num_line_sensors)
        self.brightness_value = 0

        # Timing variables
        self.last_time = ticks_us()
        self.dt = 0

        # Moving average buffers
        self.window_size = window_size
        self.buffers = [[] for _ in range(self.num_line_sensors)]
        self.positions = [i + 1 for i in range(self.num_line_sensors)]

        # Calibration data
        self.black_calib = [0] * self.num_line_sensors
        self.white_calib = [0] * self.num_line_sensors

        # Error range for scaled error output
        self.error_range = error_range

    def update(self):
        # Updates sensor readings and calculates the time difference since the last update.

        now = ticks_us()
        self.dt = ticks_diff(now, self.last_time)
        self.last_time = now

        for i, adc in enumerate(self.adc_line):
            self.line_values[i] = adc.read()

        if self.adc_brightness:
            self.brightness_value = self.adc_brightness.read()

    def get_values(self):
        # Returns the current sensor readings.
        return list(self.line_values)

    def get_brightness(self):
        # Returns the brightness sensor reading.
        return self.brightness_value

    def led_on(self):
        # Turns on the IR LED if available.
        if self.led_pin:
            self.led_pin.value(1)

    def led_off(self):
        # Turns off the IR LED if available.
        if self.led_pin:
            self.led_pin.value(0)

    def sample_inverted(self, num_samples=50, delay_ms=10):
        # Samples sensor values multiple times and inverts the readings.

        accum = [0] * self.num_line_sensors
        for _ in range(num_samples):
            self.update()
            raw = self.get_values()
            inv = [4096 - x for x in raw]
            for j in range(self.num_line_sensors):
                accum[j] += inv[j]
            pyb.delay(delay_ms)

        return [a / num_samples for a in accum]

    def calibrate(self, imu):
        # Performs calibration for black and white surfaces.

        print("Press Enter to begin calibration.")
        input()

        print("Place sensors over BLACK surface, then press Enter.")
        input()
        self.black_calib = self.sample_inverted()
        print("Black calibration complete:", self.black_calib)

        print("Place sensors over WHITE surface, then press Enter.")
        input()
        self.white_calib = self.sample_inverted()
        print("White calibration complete:", self.white_calib)

        print("Place at start to read heading, then press Enter.")
        input()

        # Store initial heading from IMU
        calib_heading = imu.read_heading()
        init.init_heading.put(int(calib_heading))
        imu.change_mode(imu.NDOF_MODE)

        print(f"Initial Heading Stored: {calib_heading:.2f} degrees")

    def line_reading(self):
        # Computes the error for line tracking based on sensor readings.

        self.update()

        raw_values = self.get_values()
        inverted = [4096 - x for x in raw_values]

        moving_avg = []
        for i in range(self.num_line_sensors):
            self.buffers[i].append(inverted[i])
            if len(self.buffers[i]) > self.window_size:
                self.buffers[i].pop(0)
            avg_val = sum(self.buffers[i]) / len(self.buffers[i])
            moving_avg.append(avg_val)

        # Normalize sensor readings
        normalized = []
        for i in range(self.num_line_sensors):
            diff = self.white_calib[i] - self.black_calib[i]
            norm = (moving_avg[i] - self.black_calib[i]) / diff if diff != 0 else 0
            norm = max(0, min(norm, 1))
            normalized.append(norm)

        # Compute weighted centroid for line position
        total_weight = sum(normalized)
        if total_weight > 0:
            centroid = sum(n * pos for n, pos in zip(normalized, self.positions)) / total_weight
        else:
            centroid = (self.num_line_sensors + 1) / 2

        center = (self.num_line_sensors + 1) / 2
        error = centroid - center

        # Scale error to the desired range
        scaled_error = max(self.error_range[0], min(error * 14, self.error_range[1]))

        return scaled_error, normalized
