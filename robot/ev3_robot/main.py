#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor, TouchSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import print, wait
from pybricks.robotics import DriveBase
from threading import Thread
from server import *
import socket
import sys

run = True


def main():
    drive_speed = 200
    s3.reset_angle(0)
    # half_scan = [45, -90, 45]
    half_scan = [45, -45]
    # full_scan = [90, -45, -90, -45, 90]
    full_scan = [90, 45, -45, -90]
    while run == True:
        if s1.pressed() == True:
            wait(1000)
            t = Thread(target=batterychk)
            t.start()
            robot.drive(drive_speed, 0)
            # add check angle and modify you can slow one motor or the other to straighten
            while run == True:
                # if s2.distance() < 300:
                #    print("Detected obsticle ahead {}".format(s2.distance()))
                #    robot.stop()
                #    direction = vision_scan(type = "full", scan_lst = [90, -45, -45, -45, -45])
                # print(type(direction))
                #    print("returned {}".format(direction))
                #    avoid_obs(direction)
                #    robot.drive(drive_speed, 0)
                result = vision_scan(type="half", center_pt=45, scan_lst=half_scan)
                print(result)
                if result == "None":
                    pass
                elif result > -5 or result < 5:
                    print("Detected obsticle ahead {}".format(s2.distance()))
                    robot.stop()
                    direction = vision_scan(type="full", center_pt=90, scan_lst=full_scan)
                    # print(type(direction))
                    # print("returned {}".format(direction))
                    avoid_obs(direction)
                    robot.drive(drive_speed, 0)
                elif result > -50 or result < -40:
                    avoid_obs(direction=45)
                elif result < 50 or result > 40:
                    avoid_obs(direction=-45)
                # while s3.angle() != 0:
                #    print("Not straight")
                #    if s3.angle() < 0:
                #        robot.drive(0, -150)
                #    else:
                #        robot.drive(0, 150)

                # robot.drive(drive_speed, 0)
                wait(700)


def control_srv():
    # Create a TCP/IP socket
    # ipaddr = socket.socket.gethostbyname(socket.gethostname())
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print(ipaddr)
    # Bind the socket to the port
    serversocket.bind(("192.168.1.165", 8000))
    # print('starting up on %s port %s' % server_address)
    serversocket.listen(5)
    while True:
        # establish a connection
        clientsocket, addr = serversocket.accept()

        print("Got a connection from %s" % str(addr))

        msg = 'Thank you for connecting' + "\r\n"
        clientsocket.send(msg.encode('ascii'))

    # clientsocket.close()


def vision_scan(type=None, center_pt=None, scan_lst=None):
    # print(scan_lst)
    motor_speed = 150
    wait_time = 10
    # center.reset_angle(0)
    # turn_degree = 90
    # scan_lst = [90, -45, -45, -45, -45]
    dist_lst = {}
    for line in scan_lst:
        # print("Scan {}".format(line))
        center.run_target(motor_speed, line)
        wait(10)
        # angle_dif = line - center.angle()
        # print(angle_dif)
        # center.run_angle(motor_speed, angle_dif)
        # wait(10)
        dist_lst[center.angle()] = s2.distance()
        wait(10)
    center.run_target(motor_speed, 0)
    # wait(10)
    # if center.angle() < 0:
    #    center.run(150)
    #    while center.angle() < 0:
    #        wait(1)
    # elif center.angle() > 0:
    #    center.run(-150)
    #    while center.angle() > 0:
    #        wait(1)
    # center.stop()

    # wait(10)
    angle_diff = 0 - center.angle()
    print(angle_diff)
    center.run_target(motor_speed, angle_diff)
    dist_lst[center.angle()] = s2.distance()
    # wait(10)

    # print(dist_lst)
    if type == "full":
        result = max(dist_lst.values())
        for key, value in dist_lst.items():
            if result == value:
                return key
    else:
        print(dist_lst)
        for key in dist_lst:
            print(dist_lst[key])
            if dist_lst[key] < 500:
                return key
            else:
                pass
        return "None"


def avoid_obs(direction=None):
    s3.reset_angle(0)
    print("Current Angle: {}".format(s3.angle()))
    robot.drive_time(-150, 0, 1000)
    if direction > 0:
        robot.drive(0, -150)
        while direction > s3.angle():
            # pass
            wait(1)
    else:
        robot.drive(0, 150)
        while direction < s3.angle():
            # pass
            wait(1)
    robot.drive(200, 0)
    return


def batterychk():
    while True:
        print("Battery level {}".format(brick.battery.voltage()))
        if brick.battery.voltage() < 5000:
            run = False
            robot.stop()
            print("Battery Low {}".format(brick.battery.voltage()))
            brick.display.text("Battery Low", (60, 50))
            while True:
                brick.light(Color.RED)
                brick.sound.beep()
                wait(500)
                brick.light(None)
                brick.sound.beep()
                # brick.sound.speak("Battery Low")
                wait(500)
        wait(2000)


if __name__ == "__main__":
    # Setup ports
    left = Motor(Port.B, Direction.COUNTERCLOCKWISE)
    right = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    center = Motor(Port.D, Direction.CLOCKWISE)
    robot = DriveBase(left, right, 56, 114)
    s1 = TouchSensor(Port.S2)
    s2 = UltrasonicSensor(Port.S1)
    s3 = GyroSensor(Port.S3)
    # main()
    # rotation_chk()
    control_srv()
    # print(vision_scan(type="full", scan_lst=[90, -45, -45, -45, -45, 90]))
    # print(vision_scan(type="half", scan_lst=[45, -45, -45, 45]))

