# ME405-Winter25-Term-Project
This repository encompasses the mecha25 team 's final report for the Winter 2025 term project for **Sam Sakaguchi** and **Timothy Chu**. This project documents everything about our Romi including what makes it unique, the desgin, pin cofiguration and coding process that made Romi drive autonomously on the course. 


##### Table of Contents  
* [The Course](#the-course)  
* [Materials and Parts](#materials-and-parts)  
* [Romi Assembly](#romi-assembly)  
* [Wiring Diagram](#wiring-diagram)
* [What makes our Romi Unique](#what-makes-our-romi-unique)
* [Kinematics](#kinematics)
* [Task Diagrams and Descriptions](#task-diagrams-and-descriptions)  
* [Finite State Machines](#finite-state-machines)  
* [Code Description](#code-description)
* [Time Trials](#time-trials)
* [Video of Romi](#video-of-romi)
* [Conclusion](#conclusion) 

# The Course

Below is the image of the course. The starting position and the ending position are the exact same for the course. 
Requirements for this course include the following:
* Hitting all 6 checkpoints labeled (CP#) in order
* Hitting the wall at some point on the course
* Attempting to get the fastest time as possible
* Cups will be put over the 5s deduction spaces and must be pushed out of the circle for those to count.

![1742152525769-57c1c358-5c8b-471f-be25-ab3d4c9f98cd_1](https://github.com/user-attachments/assets/0e8832d8-63dd-4891-ae1e-e25146b48fcb)

The tricky part about this course was the line sensing portion. With multiple different scenarios, including the diamond before CP#1, the dashed lines and the perpendicular lines, Romi would go off course from even a little bit of misalignment, making it's behavior sparatic. This line following was then followed by a grid in which Romi would have to carefully navigate through the beams, turn 90 degrees and maneuver in between two beams to regain the line following. This then is followed by the wall in which Romi would have to navigate around as well in order to return to it's starting point or the last checkpoint. 

# Materials and Parts

## Lab Provided Parts
> [!NOTE]
> These parts were provided by the Cal Poly San Luis Obispo ME405 Professor Charlie Refvem

| Qty | Part | Source |
| ------------- | ------------- | ---------|
| 2 | M2.0 x 8mm Standoff  | Lab Provided |
| 2 | M2.0 x Nylon Lock Nuts  | Lab Provided |
| 4 | M2.5 x 8mm Standoff  | Lab Provided |
| 8 | M2.5 x 10mm Standoff  | Lab Provided |
| 4 | M2.5 x 30mm Standoff  | Lab Provided |
| 4 | M2.5 x 6mm Socket Head Cap Screw  | Lab Provided |
| 4 | M2.5 x 8mm Socket Head Cap Screw  | Lab Provided |
| 4 | M2.5 x 10mm Socket Head Cap Screw  | Lab Provided |
| 12 | M2.5 Nylon Lock Nuts  | Lab Provided |
| 12 | M2.5 Nylon Washer  | Lab Provided |
| 1 | Acrylic Romi-to-Shoe Adapter  | Lab Provided |
| 1 | BNO055 IMU Breakout Board  | Lab Provided |
| 1 | Modified Shoe of Brian  | Lab Provided |
| 1 | Extra Nucleo L476RG  | Lab Provided |
| 1 | Romi Chassis w/ Wheels and Caster  | Lab Provided |
| 1 | 47k Ohm Resistor  | Lab Provided |
| 1 | 22k Ohm Resistor  | Lab Provided |

## Other sourced Parts
> [!NOTE]
> These separate parts were bought by the team

| Qty | Part | Source |
| ------------- | ------------- | ---------|
| 1 | 120pcs 20 cm Dupon Ribbon  | [Link](https://www.amazon.com/dp/B07GCY6CH7?th=1) |
| 1 | HC-05 Bluetooth Module  | [Link](https://www.amazon.com/dp/B01MQKX7VP) |
| 6 | NiMH AA Battery | [Link](https://www.amazon.com/dp/B0D2JCY87L) |
| 1 | NiMH Battery Charger | [Link](https://www.amazon.com/dp/B00JHKSLM8) |
| 1 | IR Reflectance Sensor 4mm x 13 | [Link](https://www.pololu.com/category/123/pololu-qtr-reflectance-sensors) |
| 1 | USB-Mini-B to USB-C Cable | [Link](https://www.amazon.com/dp/B082F3M1HW?th=1) |
| 1 | Bumper Switch Assembly | [Link](https://www.pololu.com/product/3674) |


# Romi Assembly

> [!NOTE]
> The Romi Assembly Construction Manual was provided by Professor Charlie Refvem and is linked here as the [Term Project Construction Manual](https://github.com/user-attachments/files/19275778/ME405_2252_Term_Project_0x01.pdf)


The Romi Robot integrates mutliple systems, including the following

* **Nucleo-L476RG** acts as the main processing unit, handling sensor data, executing algorithms, and driving the motors. From the laptop, it connects to the Shoe of Brian and communicates with other sensors like the BNO055 IMU for orientation sensing and the Reflectance Sensor for line tracking. With its processor, multiple communication interfaces (I2C, SPI, UART), it enables real-time decision-making and efficient motor control, allowing it to do operations and tasks for Romi to complete the obstacle course.

![image](https://github.com/user-attachments/assets/f068ee48-962a-4012-bbfa-ddeb9c12db73)

* **Shoe of Brian** (Picture provided by Professor Charlie Refvem) has a USB-mini-B connection, which connects the laptop with the Nucleo and prevent current back into the laptop.

![image](https://github.com/user-attachments/assets/87cfe455-d4db-431e-9dda-19f47bcdf87a)

* **Motor Drivers** are used to allow Romi to steer and allow wheel control with the **Encoders**. It uses Pulse Width Modulation (PWM) for speed controlling can set the direction via the DIR digital pin cofiguration, and enables/disables using a SLP Digital Pin.
  
* **Encoders**, attached to the Motors allow us to monitor the position and velocity using hardware timers attached to the motors. Counting in endcoder ticks, these changes in time can be used to calculate total position and velocity of Romi for each motor at any given moment, which was important in our case for when to know when we have hit CP#4
  
* **IR Sensor Array** is used for following the line, calibrating the data and putting it into a closed loop controller to read the error and change the PWM of the motors accordingly. The team uses 7 of the 13 pins available (the odd pins) to minimize the total amount of analog pins needed while also keeping a small enough spread to read the line correctly.

* **Bump Sensors** were used for multiple instances for our case. Initially, it was used to stop our Romi when triggered for ease of use, but currently, it was used to trigger a state within our main task to return to the starting position after hitting the wall.

* **BNO055 IMU Breakout Board** The IMU is a 9-axis orientation sensor that integrates an accelerometer, gyroscope, and magnetometer that uses sensor data to provide highly accurate orientation estimates

![image](https://github.com/user-attachments/assets/f6e64f59-799b-4cc5-91aa-654f3f0be253)

* **Voltage Divider** (image shown below) was used to help with the motor compensation and monitor the amount of volts Romi was running each trial. With a full set of NiMH AA batteries, the total maximum voltage output would be 6 x 1.4V = 8.4V. R1 was set to 47K ohms and R2 was set to 22K ohms  to get a similar Vout that would convert the 8.4V to 3.3V for the ADC.

  ![image](https://github.com/user-attachments/assets/5d546f19-00ff-4f6b-9dc2-f0e02807cb71)

# Wiring Diagram

# What makes our Romi Unique
Our Romi is unique for a couple of reasons. On the hardware side, it is very similar to everyone else's robot, as it has the typical motor and encoders, the IR Sensor and the bump sensor as well. What makes our Romi unique is on the coding side. This code was inevitiably our problem as we decided to a voltage divider and had multiple parameters with arbitrary numbers to maintain the consistency of Romi depending on the battery charge of Romi. This means that in order for Romi to work perfectly, the parameters had to be nearly perfect or one slight misinput could mess up the position of Romi and the error could be to great for Romi to realign. 
# Kinematics

![image](https://github.com/user-attachments/assets/67c7271a-a9e4-40f7-bf5f-ee6302cfe82b)

Romi is a small, two-wheeled differential drive robot that has two motors that can move independently. Understanding its kinematics is essential for controlling its movement accurately, even if only for simple navigation tasks. 

### Differential Drive Kinematics
Romi has a differential drive system, meaning it has two independently controlled wheels with a caster wheel providing additional balance and support. This system allows for precise control over linear and angular motion by varying the velocities of the left and right wheels.

### Forward Kinematics
The forward kinematics equations describe how wheel velocities translate into robot motion. If the left and right wheels have velocities  and , respectively, and the wheel radius is , then the linear velocity  and angular velocity  of the robot’s center are given by:

$` v = Ωr `$

$` ω = (r/w)(V_R - V_L) `$

### Yaw Angles
### Practical Considerations
Several factors influence Romi’s real-world kinematics, including:
* Wheel slippage and friction: Imperfections in wheel traction can affect motion accuracy.
* Sensor feedback: Encoders can improve control by providing real-time wheel velocity data.
* Control algorithms: Implementing PID controllers can help maintain stable motion and correct deviations from intended trajectories.

# Task Diagrams and Descriptions

# Finite State Machines

# Code Description

**main.py:**
Our main.py code will manage all of the other functions and files that controls individual Romi components and software that processes data to make motor decisions. 
Main includes the following functions, tasks and operations
* A battery regulator function that takes the value from a voltage divider from the battery and readjusts the motors in accordance to the battery level and expected battery level.
* Line sensor initialization as well as start calibration to get the heading of Romi at start of track, this heading will be used to help adjust Romi heading at the final task at the grid.
* Line sensor task will constantly grab the scaled error after giving the PID controller the linesensor readings.
* Encoder task update will initialize the pins used for the left and right encoder and constantly update to push the position to a queue which we will pull from to track distance traveled to use later as a conditional for final task.
* Final task which occurs when we reach the desired distance (113) which is the end of the lined track and beginning of the grid and cage part. The final task will stop the Romi, then swivel to 180 degrees offset of the initial recorded heading to perfectly align itself for forward movement through the cage. the robot will then move forward a set distance, then turn 90 degrees towards the obstacle wall, then move forward before hitting the wall, and turn -90 degrees before collision, then move forward a set distance to hit the second cup for a time deduction, at which the Romi will turn -90 degrees, move forward a set distance, and turn -90 degrees one more time before moving forward into the final checkpoint and start area.
* Scheduler processes all of the following tasks: Linesensor, PID controller, Left Motor, Right Motor, Encoder Update. Additionally, to save time for the scheduler and to ensure all tasks are performed on time, we do not use any prints and optimize all tasks that need to run in this main schedule. Lastly, to save even more time, tasks that only run once such as the final task do not run at all until certain conditions: Encoder distance reading is at 113, and line sensor reads roughly all white to indicate the end of the path.
* Keyboard interrupt to stop the motors and disable them when we restart the REPL.

**bump_sensor.py:**
Our bump_sensor.py sets up external interrupts for four bump sensors and provides a cooperative task to react to bump_flag. This allows the Romi to stop when bump sensors are triggered.

**encoder.py:**
Our encoder.py implements an encoder class for tracking position and velocity. It utilizes a hardware timer in encoder mode to count pulses from a quadrature encoder, allowing for real-time position and velocity calculations. We have an update function that updates the encoder count, position, and velocity calculations and corrects for overflow/underflow of the 16-bit counter.

**imu.py:**
Our imu.py provides an interface for the BNO055 IMU sensor using I2C. It supports reading sensor data, calibration, and mode configuration. We have functions for calibration status as well as a function that reads and returns the calibration coefficient from the sensor for the accelerometer, magnetometer, and gyroscope. Functions to read the heading, Euler, angular velocity, acceleration, and magnetic field. For this project, only the heading is used for motor control

**left_motor.py & right_motor.py:**
Our left_motor.py and right_motor.py


# Time Trials

# Video of Romi

# Conclusion
