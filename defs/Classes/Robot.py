import urx
import time
from Gripper import *
from enum import Enum


class ROBOT_SIDE(Enum):
    LEFT = 1
    RIGHT = 2


class Robot:
    def __init__(self, ip, side: ROBOT_SIDE):
        self.ip = ip
        self.side = side
        self.robot = None 
        self.homePosition = (0.25, -0.22, 0.20, 0, 3.14, 0)
        self.sentBlocks = 0
        self.pos_multiplyer = 0.06
        self.block_y_pos = -0.22 - (self.sentBlocks * self.pos_multiplyer)
    
    def initRobot(self):
        self.robot = urx.Robot(self.ip, use_rt=True, urFirm=5.1)
    
    def home(self):
        self.move(self.homePosition)

    def setTCP(self, tcp):
        self.robot.set_tcp(tcp)
        time.sleep(0.3)

    def move(self, location, moveWait=True):
        #moves robot
        self.robot.movex("movel", location,wait=moveWait, acc=0.5, vel=0.8, relative=False, threshold=None)
        if moveWait == False:
            time.sleep(0.1)

    def activateAndOpenGripper(self):
        #activates gripper. only needed once per power cycle
        self.robot.send_program(rq_activate())
        time.sleep(2.5)
        #sets speed of gripper to max
        self.robot.send_program(rq_set_speed(1))
        time.sleep(0.1)
        #sets force of gripper to a low value
        self.robot.send_program(rq_set_force(10))
        time.sleep(0.1)
        self.robot.send_program(rq_open())
        time.sleep(2)
    
    def openGripper(self):
        self.robot.send_program(rq_open_and_wait())
    
    def closeGripper(self):
        self.robot.send_program(rq_close())
        time.sleep(3)
    
    def pickUpFromConveyor(self):
        self.sentBlocks += 1

        #positions x, y, z, rx, ry, rz
        startPosition = 0.25, -0.22, 0.20, 0, 3.14, 0
        pos2 = 0.20, 0.10, 0.30, 0, 3.14, 0
        pos3 = 0.03, 0.30, 0.30, 0, 3.14, 0
        pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
        pos5 = 0.03, 0.30, 0.15, 0, 3.14, 0
        pos6 = 0.25, self.block_y_pos, 0.30, 0, 3.14, 0
        pos7 = 0.25, self.block_y_pos, 0.20, 0, 3.14, 0

        self.openGripper()

        self.move(location = startPosition)
        self.move(location = pos2)
        self.move(location = pos3)
        self.move(location = pos4)
        self.move(location = pos5)

        self.closeGripper()

        self.move(location = pos4)
        self.move(location = pos3)
        self.move(location = pos2)
        self.move(location = startPosition)
        self.move(location = pos6)
        self.move(location = pos7)

        self.openGripper()
        time.sleep(2)

        self.move(location = pos6)
        self.move(location = startPosition)

    def pickUpFromWorkingSpace(self, positionPickup):
        self.move(location = positionPickup)
        self.closeGripper()
    
    def placeOnConveyor(self):
        homePosition = 0.25, -0.22, 0.20, 0, 3.14, 0
        pos2 = 0.15, -0.10, 0.20, 0, 3.14, 0
        pos3 = 0.15, 0.10, 0.20, 0, 3.14, 0
        pos4 = 0.15, 0.30, 0.20, 0, 3.14, 0
        pos5 = -0.01, 0.28, 0.01, 0, 3.14, 0

        # Go to home position
        self.move(location = self.homePosition)
        # Move from home position towards conveyor belt
        self.move(location = pos2)
        # Even closer to the conveyor belt
        self.move(location = pos3)
        # Straight over drop location on conveyor belt
        self.move(location = pos4)
        # Final drop on conveyor
        self.move(location = pos5)
        # Open to drop block
        self.openGripper()
        time.sleep(2)
        # Move away from block
        self.move(location = pos4)
        # Move from the conveyor belt towards home position
        self.move(location = pos3)
        # Even closer to home position
        self.move(location = pos2)
        # Back at home position
        self.move(location = self.homePosition)
        time.sleep(0.5)
    
    def close(self):
        self.robot.close()


if __name__ == "__main__":
    print("CREATING ROBOT OBJECCT")
    robotLeft = Robot("10.1.1.6")
    robotRight = Robot("10.1.1.5")

    print("INIT ROBOT")
    robotRight.initRobot()
    print("SETTING TCP")
    robotRight.setTCP( (0,0,0.16,0,0,0) )
    time.sleep(3)
    print("ACTIVATING GRIPPER")
    robotRight.activateAndOpenGripper()
    print("OPEN GRIPPER")
    robotRight.openGripper()
    time.sleep(2)
    print("CLOSE GRIPPER")
    robotRight.closeGripper()
    time.sleep(2)
    print("HOME")
    robotRight.home()

    print("INIT ROBOT LEF")
    robotLeft.initRobot()
    robotLeft.setTCP( (0,0,0.16,0,0,0) )
    time.sleep(3)
    robotLeft.activateAndOpenGripper()
    robotLeft.openGripper()
    time.sleep(2)
    robotLeft.closeGripper()
    time.sleep(2)
    robotLeft.home()

    robotLeft.close()
    robotLeft.close()



