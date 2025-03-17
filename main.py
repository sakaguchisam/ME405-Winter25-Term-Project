"""
main.py

Project: ME405 ROMI Final Project
Date: Mar 16, 2025
Authors: Sam Sakaguchi, Timothy Chu

Summary:
Manages all functions and files that control individual Romi components 
and processes data to make motor decisions. The main script includes:

1. **Battery Regulation:** 
   - Reads battery voltage from a voltage divider and adjusts motor effort 
     to maintain expected performance despite battery depletion.

2. **Line Sensor Initialization & Calibration:** 
   - Initializes the line sensors and performs calibration.
   - Records the initial heading of the Romi at the start of the track.
   - This heading is used for realignment in the final task.

3. **Line Sensor Task:** 
   - Continuously retrieves the scaled error from the line sensor.
   - Provides this error to the PID controller for real-time corrections.

4. **Encoder Update Task:** 
   - Initializes the left and right encoders.
   - Continuously updates and pushes position data into a queue.
   - This data is used to track distance traveled and determine 
     when the final task should begin.

5. **Final Task:** 
   - Triggers when the desired distance (113) is reached, marking 
     the end of the line track and the beginning of the grid.
   - The Romi stops, swivels to a 180-degree offset of the initial 
     heading for perfect alignment.
   - Executes a sequence of movements:
     1. Moves forward a set distance.
     2. Turns 90 degrees toward the obstacle wall.
     3. Moves forward before reaching the wall.
     4. Turns -90 degrees to avoid collision.
     5. Moves forward to hit the second cup for a time deduction.
     6. Turns -90 degrees and moves forward.
     7. Turns -90 degrees again before reaching the final checkpoint.

6. **Task Scheduler:** 
   - Manages critical tasks: Line Sensor, PID Controller, Left Motor, 
     Right Motor, and Encoder Update.
   - Optimized for efficiency by avoiding prints during execution.
   - Tasks that only run once (e.g., Final Task) are only executed 
     when conditions are met (encoder distance ≥ 113 and white line detected).

7. **Keyboard Interrupt Handling:** 
   - Stops and disables motors safely when the REPL is restarted.
"""

import cotask
from cotask import Task, task_list
from pyb import Pin, ADC
import init
import gc
from time import ticks_ms
from task_share import Share

# Ensure shared variables are initialized
init.final_flag = Share('b', thread_protect=True, name="Final Flag")
init.final_flag.put(0)

init.current_encoder_left = Share('f', thread_protect=True, name="Current Encoder Left")
init.current_encoder_left.put(0)

# Import drivers and tasks
from linesensor import LineSensorDriver
from PID_controller import PID_value
from left_motor import task_left_motor, left_motor
from right_motor import task_right_motor, right_motor
from imu import BNO055
from bump_sensor import init_bump_sensors, task_bump_handling
from encoder import Encoder

# Battery Voltage Measurement Setup
battery_pin = Pin('PC4')
battery_adc = ADC(battery_pin)

def read_battery_voltage():
    raw_val = battery_adc.read()
    v_adc = (raw_val / 4095.0) * 3.3
    return v_adc * (69.0 / 22.0)

init_voltage = read_battery_voltage()
V_nominal = 7.2
computed_multiplier = 1.0 if init_voltage < 0.1 else V_nominal / init_voltage
print("Initial battery voltage: %.2f V, constant multiplier: %.2f" % (init_voltage, computed_multiplier))
init.constant_multiplier.put(computed_multiplier)

# Line Sensor Configuration
line_sensor_pins = ['PA0', 'PA1', 'PA4', 'PB0', 'PC1', 'PC0', 'PC3']
brightness_pin = 'PC2'
window_size = 10

imu = BNO055(SDA='PB9', SCL='PB8', RST='PA15', bus=1)
imu.initialize()

sensor_driver = LineSensorDriver(line_pins=line_sensor_pins, brightness_pin=brightness_pin, window_size=window_size)
sensor_driver.calibrate(imu)
init.bump_flag = False

input("Calibration complete. Press Enter to start the robot (motors will now move).")

# Line Sensor Task
def task_linesensor_wrapper():
    while True:
        scaled_error, _ = sensor_driver.line_reading()
        if not init.collection_data_queue.full():
            init.collection_data_queue.put(scaled_error)
        yield 0

# Encoder Update Task
def task_encoder_update_real():
    left_enc = Encoder(tim=1, chA_pin='PA9', chB_pin='PA8')
    right_enc = Encoder(tim=8, chA_pin='PC7', chB_pin='PC6')
    while True:
        left_enc.update()
        right_enc.update()
        if not init.encoder_left_data_queue.full():
            init.encoder_left_data_queue.put(left_enc.get_position())
        if not init.encoder_right_data_queue.full():
            init.encoder_right_data_queue.put(right_enc.get_position())
        init.current_encoder_left.put(left_enc.get_position())
        yield 0

# Final Task: Monitors encoder and adjusts heading if needed
def task_final():
    while True:
        left_val = init.current_encoder_left.get()
        if left_val >= 113:
            init.final_flag.put(1)

        if init.final_flag.get() == 1:
            break
        yield 0

    while True:
        current_heading = imu.read_heading()
        target_heading = (init.init_heading.get() - 180) % 360
        heading_error = target_heading - current_heading
        heading_error = (heading_error + 180) % 360 - 180

        if abs(heading_error) > 2:
            correction = init.kp_value.get() * heading_error / 100
            init.left_effort.put(int(correction))
            init.right_effort.put(int(-correction))
        else:
            init.left_effort.put(25)
            init.right_effort.put(25)
        yield 0

# Initialize Bump Sensors
init_bump_sensors()

# Enable Motors
left_motor.enable()
right_motor.enable()

# Create Tasks
task_list.append(Task(task_bump_handling, name="Bump Handler", priority=3, period=20))
task_list.append(Task(task_linesensor_wrapper, name="Line Sensor", priority=2, period=11))
task_list.append(Task(PID_value, name="PID Controller", priority=1, period=11))
task_list.append(Task(task_left_motor, name="Left Motor", priority=0, period=11))
task_list.append(Task(task_right_motor, name="Right Motor", priority=0, period=11))
task_list.append(Task(task_encoder_update_real, name="Encoder Update", priority=0, period=25))
task_list.append(Task(task_final, name="Final Task", priority=0, period=50))
gc.collect()

# Main Loop
if __name__ == "__main__":
    print("Starting all tasks. Press any bump sensor to stop motors.")
    while True:
        try:
            task_list.pri_sched()
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected: stopping motors.")
            left_motor.update(0)
            right_motor.update(0)
            left_motor.disable()
            right_motor.disable()
            break
        except Exception as e:
            print("Unhandled exception:", e)
            left_motor.update(0)
            right_motor.update(0)
            left_motor.disable()
            right_motor.disable()
            raise
    print('\n' + str(cotask.task_list))
