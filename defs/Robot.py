import urx
import time
from Gripper import *

class Robot:
    def __init__(self, ip, homePos):
        self.ip = ip
        self.robot = None 
        self.homePosition = homePos
    
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
    
    def close(self):
        self.robot.close()


if __name__ == "__main__":
    print("CREATING ROBOT OBJECCT")
    robotLeft = Robot("10.1.1.6", (0.25, -0.22, 0.20, 0, 3.14, 0) )
    robotRight = Robot("10.1.1.5", (0.25, -0.22, 0.20, 0, 3.14, 0) )

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
    centerViaPointBeforeHomePos = 0,-0.3,0.2,0,3.14,0 
    robotRight.move(centerViaPointBeforeHomePos)

    print("INIT ROBOT LEF")
    robotLeft.initRobot()
    robotLeft.setTCP( (0,0,0.16,0,0,0) )
    time.sleep(3)
    robotLeft.activateAndOpenGripper()

    time.sleep(2)
    robotLeft.closeGripper()
    robotLeft.openGripper()
    time.sleep(2)
    robotLeft.home()
    robotLeft.move(centerViaPointBeforeHomePos)
    robotLeft.close()
    robotLeft.close()



