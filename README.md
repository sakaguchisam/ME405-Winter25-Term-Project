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

The tricky part about this course was the line sensing portion. With multiple different scenarios, including the diamond before CP#1, the dashed lines and the perpendicular lines, Romi would go off course from even a little bit of misalignment, making it's behavior sparatic. This line following was then followed by a grid in which Romi would have to carefully navigate through the beams, turn 90 degrees and maneuver in between two beams to regain the line following. This then is followed by the wall in which Romi would have to navigate around as well in order to return to it's starting point of the last checkpoint. 

# Materials and Parts

## Lab Provided Parts
These parts were provided by the Cal Poly San Luis Obispo ME405 Professor Charlie Refvem

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
These separate parts were bought by the team
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

* **Nucleo L476RG** 
* **Motor Drivers** are used to allow Romi to steer and allow wheel control with the **Encoders**
* **Encoders**, attached to the Motors allow us to monitor the position and velocity
* **IR Sensor Array** is used for following the line, calibrating the data and putting it into a closed loop controller to read the error and change the PWM of the motors accordingly
* **Bump Sensors** were used for multiple instances for our case. Initially, it was used to stop our Romi when triggered for ease of use, but currently, it was used to trigger a state within our main task to return to the starting position after hitting the wall.
* **BNO055 IMU Breakout Board** The IMU is a 9-axis orientation sensor that integrates an accelerometer, gyroscope, and magnetometer that uses sensor data to provide highly accurate orientation estimates
* **Voltage Divider** (image shown below) was used to help with the motor compensation and monitor the amount of volts Romi was running each trial. With a full set of NiMH AA batteries, the total maximum voltage output would be 6 x 1.4V = 8.4V. R1 was set to 47K ohms and R2 was set to 22K ohms  to get a similar Vout that would convert the 8.4V to 3.3V for the ADC.

  ![image](https://github.com/user-attachments/assets/5d546f19-00ff-4f6b-9dc2-f0e02807cb71)

# Wiring Diagram

# What makes our Romi Unique
Our Romi is unique for a couple of reasons. On the hardware side, it is very similar to everyone else's robot, as it has the typical motor and encoders, the IR Sensor and the bump sensor as well. What makes our Romi unique is on the coding side. This code was inevitiably our problem as we decided to a voltage divider and had multiple parameters with arbitrary numbers to maintain the consistency of Romi depending on the battery charge of Romi. 
# Kinematics

# Task Diagrams and Descriptions

# Finite State Machines

# Code Description

# Time Trials

# Video of Romi

# Conclusion
