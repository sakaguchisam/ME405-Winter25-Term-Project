"""
imu.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
This module provides an interface for the BNO055 IMU sensor using I2C.
It supports reading sensor data, calibration, and mode configuration.
"""

import init
import struct
from pyb import I2C, Pin, delay
from struct import unpack_from, calcsize
from left_motor import left_motor
from right_motor import right_motor
import PID_controller

class BNO055:
    DEV_ADDR = const(0x28)

    class reg:
        CHIP_ID      = (const(0x00), b"<B")
        OPR_MODE     = (const(0x3D), b"<B")
        PWR_MODE     = (const(0x3E), b"<B")
        UNIT_SEL     = (const(0x3B), b"<B")
        SYS_TRIGGER  = (const(0x3F), b"<B")
        CAL_STAT     = (const(0x35), b"<B")
        EUL_DATA_ALL = (const(0x1A), b"<hhh")
        ACC_DATA     = (const(0x08), b"<hhh")
        GYR_DATA     = (const(0x14), b"<hhh")
        MAG_DATA     = (const(0x0E), b"<hhh")
        ACC_OFFSET   = (const(0x55), b"<hhhh")
        MAG_OFFSET   = (const(0x5B), b"<hhhh")
        GYR_OFFSET   = (const(0x61), b"<hhhh")

    CONFIG_MODE = const(0x00)
    NDOF_MODE   = const(0x0C)
    IMU_MODE    = const(0x08)

    def __init__(self, SDA, SCL, RST, bus=1):
        # Initializes the BNO055 sensor and resets it.

        self.SDA = Pin('PB9', mode=Pin.AF_OD)
        self.SCL = Pin('PB8', mode=Pin.AF_OD)
        self.RST = Pin('PA15', mode=Pin.OUT_PP)

        self.RST.low()
        delay(10)
        self.RST.high()
        delay(1000)

        # Initialize I2C communication
        self.i2c = I2C(bus, I2C.MASTER, baudrate=400000)
        self._buf = const(22)  

    def _write_reg(self, reg, value):
        # Writes a single byte to a register.
        self.i2c.mem_write(bytearray([value]), self.DEV_ADDR, reg[0])

    def _read_reg(self, reg):
        # Reads a register and unpacks the data based on its format.
        length = calcsize(reg[1])
        buf = bytearray(length)
        self.i2c.mem_read(buf, self.DEV_ADDR, reg[0])
        return unpack_from(reg[1], buf)

    def change_mode(self, mode):
        # Changes the operation mode of the sensor.
        self._write_reg(self.reg.OPR_MODE, self.CONFIG_MODE)
        delay(10)
        self._write_reg(self.reg.OPR_MODE, mode)
        delay(20)

    def get_calibrate_status(self):
        # Returns the current calibration status.
        calib_stat = self._read_reg(self.reg.CAL_STAT)[0]
        return {
            "sys":   (calib_stat >> 6) & 0x03,
            "gyro":  (calib_stat >> 4) & 0x03,
            "accel": (calib_stat >> 2) & 0x03,
            "mag":   calib_stat & 0x03,
        }

    def get_calibrate_coeff(self):
        # Reads the calibration coefficients from the sensor.
        acc_offset = self._read_reg(self.reg.ACC_OFFSET)
        mag_offset = self._read_reg(self.reg.MAG_OFFSET)
        gyr_offset = self._read_reg(self.reg.GYR_OFFSET)
        return acc_offset, mag_offset, gyr_offset

    def write_calibrate_coeff(self, acc_offset, mag_offset, gyr_offset):
        # Writes calibration coefficients to the sensor.
        self.change_mode(self.CONFIG_MODE)
        delay(10)
        self.i2c.mem_write(bytes(acc_offset), self.DEV_ADDR, self.reg.ACC_OFFSET[0])
        self.i2c.mem_write(bytes(mag_offset), self.DEV_ADDR, self.reg.MAG_OFFSET[0])
        self.i2c.mem_write(bytes(gyr_offset), self.DEV_ADDR, self.reg.GYR_OFFSET[0])
        self.change_mode(self.NDOF_MODE)
        delay(20)

    def read_euler(self):
        # Reads Euler angles (heading, roll, pitch) from the sensor.
        data_euler = bytearray(6)
        self.i2c.mem_read(data_euler, self.DEV_ADDR, self.reg.EUL_DATA_ALL[0])
        head, roll, pitch = struct.unpack("<hhh", data_euler)
        return head / 16, roll / 16, pitch / 16

    def read_heading(self):
        # Reads only the heading (yaw) angle.
        heading_struct = bytearray(2)
        self.i2c.mem_read(heading_struct, self.DEV_ADDR, self.reg.EUL_DATA_ALL[0])
        heading = struct.unpack("<h", heading_struct)[0]
        return heading / 16

    def read_angular_velocity(self):
        # Reads gyroscope data (angular velocity).
        return self._read_reg(self.reg.GYR_DATA)

    def read_acceleration(self):
        # Reads accelerometer data.
        return self._read_reg(self.reg.ACC_DATA)

    def read_magnetic_field(self):
        # Reads magnetometer data.
        return self._read_reg(self.reg.MAG_DATA)

    def initialize(self):
        # Initializes sensor settings and sets it to NDOF mode.
        self.change_mode(self.CONFIG_MODE)
        delay(50)
        self._write_reg(self.reg.PWR_MODE, 0x00)
        self._write_reg(self.reg.UNIT_SEL, 0x00)
        self.change_mode(self.NDOF_MODE)
        delay(50)
