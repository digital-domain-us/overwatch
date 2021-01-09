#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.tools import print, wait
from pybricks.robotics import DriveBase

center = Motor(Port.D)
print(center.angle())