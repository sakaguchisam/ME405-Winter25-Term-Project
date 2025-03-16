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

The tricky part about this course was the line sensing portion. With multiple different scenarios, including the diamond before CP#1, the dashed lines and the perpendicular lines, Romi would go off course from even a little bit of misalignment, making it's behavior sparatic.

# Materials and Parts

| Part  | Quantity | Link |
| ------------- | ------------- | ---------|
| Content Cell  | Content Cell  | contnet |
| Content Cell  | Content Cell  | content |

# Romi Assembly

The Romi Robot integrates mutliple systems, including the following

* **Motor Drivers** These motors are used to allow Romi to steer and allow wheel control with the **Encoders**
* **Encoders** These encoders, attached to the Motors allow us to monitor the position, velocity
* **IR Sensor Array** This IR sensor is used for following the line and calibrating it and putting it into a closed loop controller to read the error and change the PWM of the motors
* **Bump Sensors** The bump sensors were used for multiple instances for our case. Initially, it was used to stop our Romi when triggered for ease of use, but currently, it was used to trigger a state within our main task to return to the starting position after hitting the wall.

# Wiring Diagram

# What makes our Romi Unique

# Kinematics

# Task Diagrams and Descriptions

# Finite State Machines

# Code Description

# Time Trials

# Video of Romi

# Conclusion
