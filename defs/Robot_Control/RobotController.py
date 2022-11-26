import urx
from Gripper import *
#import urllib.request
import time
import ConveyorController as CC
import detect2Objects as d2o

sentBlocks = 0
pos_multiplyer = 0.06
block_y_pos = -0.22 - (sentBlocks*pos_multiplyer)

def activateAndOpenGripper(rob):
    #activates gripper. only needed once per power cycle
    rob.send_program(rq_activate())
    time.sleep(2.5)
    #sets speed of gripper to max
    rob.send_program(rq_set_speed(1))
    time.sleep(0.1)
    #sets force of gripper to a low value
    rob.send_program(rq_set_force(10))
    time.sleep(0.1)
    rob.send_program(rq_open())
    time.sleep(2)

def pickUpFromConveyor(rob):
    global block_y_pos

    #positions x, y, z, rx, ry, rz
    pos1 = 0.10, -0.30, 0.40, 0, 3.14, 0
    pos2 = 0.20, 0.10, 0.40, 0, 3.14, 0
    pos3 = 0.03, 0.30, 0.40, 0, 3.14, 0
    pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
    pos5 = 0.03, 0.30, 0.15, 0, 3.14, 0
    
    pos6 = 0.25, block_y_pos, 0.30, 0, 3.14, 0
    pos7 = 0.25, block_y_pos, 0.20, 0, 3.14, 0
    
    move(rob, pos1)
    move(rob, pos2)
    move(rob, pos3)
    move(rob, pos4)
    move(rob, pos5)

    rob.send_program(rq_close())
    time.sleep(3)

    move(rob, pos4)
    move(rob, pos3)
    move(rob, pos2)
    move(rob, pos1)
    move(rob, pos6)
    move(rob, pos7)

    rob.send_program(rq_open())
    time.sleep(2)

    move(rob, pos6)
    move(rob, pos1)

    
def sendLeftToRight(rob, rob2):
    print("[GETTING X,Y FROM LEFT CAMERA]")
    x,y = d2o.checkLeftCamera()

    print("[VALIDATING X AND Y]")
    if (x == None or y == None):
        x, y = d2o.checkLeftCamera()

    print(f"[POST VALIDATION X AND Y][X = {x}, Y = {y}]")
    positionPickUp = (x,y,0.40,0,3.14,0)

    print("[MOVING ROBOT 2]")
    positionPickUpDown = (x,y,0.15,0,3.14,0)
    move(rob2, positionPickUp)
    move(rob2, positionPickUpDown)
    rob2.send_program(rq_close())
    time.sleep(3)

    print("[FINISHED MOVING ROBOT 2]")
    time.sleep(3)
    sensorvalue = 0
    sensorValue = CC.checkSensorReadingsLeft()
    time.sleep(2)
    print("DONE CHECKING SENSORS")
    if sensorValue != 0 or sensorValue != None:
        print("INSIDE IF")
        pickUpFromConveyor(rob)
        global sentBlocks, block_y_pos 
        sentBlocks += 1
        block_y_pos = -0.22 - (sentBlocks*pos_multiplyer)

    print("DONE WITH sendLeftToRight")

def sendRightToLeft():
    CC.checkSensorReadingsRight()
    

def pickupObjectLeftSide(rob):
    print("[GETTING X,Y FROM LEFT CAMERA]")
    x, y = d2o.checkLeftCamera() 
    time.sleep(2)


    print(f"[X = {x}, Y = {y}]")
    positionPickUp = (x,y,0.40,0,3.14,0)
    positionPickUpDown = (x,y,0.15,0,3.14,0)
    
    print("[MOVING ROBOT 2]")
    move(rob, positionPickUp)
    move(rob, positionPickUpDown)

    rob.send_program(rq_close())
    time.sleep(3)

    print("[FINISHED MOVING ROBOT 2]")
    time.sleep(3)


def move(robot, location, moveWait=True):
    #moves robot
    robot.movex("movel", location,wait=moveWait, acc=0.5, vel=0.8, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)



if __name__ =="__main__":
    #r1="10.1.1.5"
    #rob = urx.Robot(r1, use_rt=True, urFirm=5.1)

    r2="10.1.1.6"
    rob2 = urx.Robot(r2, use_rt=True, urFirm=5.1)

    #activateAndOpenGripper(rob)
    activateAndOpenGripper(rob2)

    '''
    for i in range(4):
        sendLeftToRight(rob)
        time.sleep(2)
    '''
    #sendLeftToRight(rob, rob2)
    #rob.close()

    pickupObjectLeftSide(rob2)

    rob2.close()