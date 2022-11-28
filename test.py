import urx
import time

r1="10.1.1.6"
r2="10.1.1.5"

robLeft = urx.Robot(r1, use_rt=True, urFirm=5.1)
robRight = urx.Robot(r2, use_rt=True, urFirm=5.1)

def move(robot, location, moveWait=True):
    #moves robot
    robot.movex("movej", location,wait=moveWait, acc=0.5, vel=0.8, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)

homePositionLeft = 0.25, -0.22, 0.20, 0, 3.14, 0
via1 = 0.15, -0.22, 0.20, 0, 3.14, 0
move(robLeft, homePositionLeft)
time.sleep(3)
move(robLeft, via1)
time.sleep(3)