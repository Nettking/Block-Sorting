import time
from Gripper import *
import ConveyorController as CC
import Classes.Camera as cam
import Classes.Robot as robot


sentBlocksL2R = 0
sentBlocksR2L = 0
pos_multiplyer = 0.06
block_y_posL2R = -0.22 - (sentBlocksL2R*pos_multiplyer)
block_y_posR2L = -0.22 - (sentBlocksR2L*pos_multiplyer)

cameraLeft = cam.Camera("10.1.1.8", "left")
cameraRight = cam.Camera("10.1.1.7", "Right")
rob = robot.robLeft
rob2 = robot.robRight

def move(robot, location, moveWait=True):
    #moves robot
    robot.movex("movej", location,wait=moveWait, acc=0.5, vel=0.8, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)



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

def pickUpFromConveyor(rob, from_side):
    global block_y_pos, sentBlocksL2R, sentBlocksR2L
    if from_side == "left":
        sentBlocksL2R += 1
        block_y_pos = block_y_posL2R
    if from_side == "right":
        sentBlocksR2L += 1
        block_y_pos = block_y_posR2L
    
    #positions x, y, z, rx, ry, rz
    startPosition = 0.25, -0.22, 0.20, 0, 3.14, 0
    pos2 = 0.20, 0.10, 0.30, 0, 3.14, 0
    pos3 = 0.03, 0.30, 0.30, 0, 3.14, 0
    pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
    pos5 = 0.03, 0.30, 0.15, 0, 3.14, 0
    
    pos6 = 0.25, block_y_pos, 0.30, 0, 3.14, 0
    pos7 = 0.25, block_y_pos, 0.20, 0, 3.14, 0
    rob.send_program(rq_open_and_wait())
    move(rob, startPosition)
    move(rob, pos2)
    move(rob, pos3)
    move(rob, pos4)
    move(rob, pos5)

    rob.send_program(rq_close())
    time.sleep(3)

    move(rob, pos4)
    move(rob, pos3)
    move(rob, pos2)
    move(rob, startPosition)
    move(rob, pos6)
    move(rob, pos7)

    rob.send_program(rq_open())
    time.sleep(2)

    move(rob, pos6)
    move(rob, startPosition)

    
def getImputFromLeftCamera():
    print("[GETTING X,Y FROM LEFT CAMERA]")
    x,y = cam.resultCameraLeft
    return x,y
    

def setPositionFromCameraInputLeft():
    x,y = getImputFromLeftCamera()
    print(f"[POST VALIDATION X AND Y][X = {x}, Y = {y}]")
    # Left side has reversed y-value 
    positionPickUp = (x,-y,0.20,0.05,3.14,0)
    #positionPickUpDown = (x,y,0.15,0,3.14,0)
    return positionPickUp


def getImputFromRightCamera():
    print("[GETTING X,Y FROM Right CAMERA]")
    x,y = cam.resultCameraRight
    return x,y
    


def setPositionFromCameraInputRight():
    x,y = getImputFromRightCamera()
    print(f"[POST VALIDATION X AND Y][X = {x}, Y = {y}]")
    # Left side has reversed y-value 
    positionPickUp = (x,y,0.20,0.05,3.14,0)
    #positionPickUpDown = (x,y,0.15,0,3.14,0)
    return positionPickUp











def placeObjectLeftOnConveyor(rob):
    homePosition = 0.25, -0.22, 0.20, 0, 3.14, 0
    pos2 = 0.15, -0.10, 0.20, 0, 3.14, 0
    pos3 = 0.08, 0.10, 0.20, 0, 3.14, 0
    pos4 = 0.03, 0.30, 0.20, 0, 3.14, 0
    pos5 = 0.03, 0.30, 0.15, 0, 3.14, 0
    # Go to home position
    move(rob, homePosition)
    # Move from home position towards conveyor belt
    move(rob, pos2)
    # Even closer to the conveyor belt
    move(rob, pos3)
    # Straight over drop location on conveyor belt
    move(rob, pos4)
    # Final drop on conveyor
    move(rob, pos5)
    # Open to drop block
    rob.send_program(rq_open())
    # Move away from block
    move(rob, pos4)
    # Move from the conveyor belt towards home position
    move(rob, pos3)
    # Even closer to home position
    move(rob, pos2)
    # Back at home position
    move(rob, homePosition)
    time.sleep(0.5)

def placeObjectRightOnConveyor(rob):
    homePosition = 0.25, -0.22, 0.20, 0, 3.14, 0
    pos2 = 0.15, -0.10, 0.20, 0, 3.14, 0
    pos3 = 0.08, 0.10, 0.20, 0, 3.14, 0
    pos4 = 0.03, 0.30, 0.20, 0, 3.14, 0
    pos5 = 0.03, 0.30, 0.15, 0, 3.14, 0
    # Go to home position
    move(rob, homePosition)
    # Move from home position towards conveyor belt
    move(rob, pos2)
    # Even closer to the conveyor belt
    move(rob, pos3)
    # Straight over drop location on conveyor belt
    move(rob, pos4)
    # Final drop on conveyor
    move(rob, pos5)
    # Open to drop block
    rob.send_program(rq_open())
    # Move away from block
    move(rob, pos4)
    # Move from the conveyor belt towards home position
    move(rob, pos3)
    # Even closer to home position
    move(rob, pos2)
    # Back at home position
    move(rob, homePosition)
    time.sleep(0.5)


def pickupObjectLeftSide(rob):

    positionPickUp = setPositionFromCameraInputLeft()

    print(positionPickUp)
    
    print("[MOVING ROBOT 2]")
    move(rob, positionPickUp)

    rob.send_program(rq_close())
    time.sleep(3)

    print("[FINISHED MOVING ROBOT 2]")
    time.sleep(3)

def pickupObjectRightSide(rob):

    positionPickUp = setPositionFromCameraInputRight()

    print(positionPickUp)
    
    print("[MOVING ROBOT 2]")
    move(rob, positionPickUp)

    rob.send_program(rq_close())
    time.sleep(3)

    print("[FINISHED MOVING ROBOT 2]")
    time.sleep(3)


def sendLeftToRight():
    # Find block
    pickupObjectLeftSide(rob)
    # Place on conveyor
    placeObjectLeftOnConveyor(rob)
    # Send block if on conveyor
    CC.checkSensorReadingsLeft()
    # Place block on home area
    pickUpFromConveyor(rob2, "left")
    


def sendRightToLeft():
    # Find block
    pickupObjectRightSide(rob2)
    # Place on conveyor
    placeObjectRightOnConveyor(rob2)
    # Send block if on conveyor
    CC.checkSensorReadingsRight()
    # Place block on home area
    pickUpFromConveyor(rob, "right")

    





if __name__ =="__main__":
    #r1="10.1.1.5"
    #rob = urx.Robot(r1, use_rt=True, urFirm=5.1)

    #
    #activateAndOpenGripper(rob)
    #activateAndOpenGripper(rob2)
    #x,y = getImputFromLeftCamera()
    #positionPickUp = 0.2,0.2,0.40,0,3.14,0
    #position = setPositionFromCameraInputLeft()
    #    print(cam.resultCameraLeft)
    #    move(rob, positionPickUp)
    #sendLeftToRight(rob)
    #froskPos = 0.2, 0.2, 0.2, 0, 3.14, 0
    #move(rob, froskPos, True)
    #    pickUpFromConveyor(rob2)
    '''
    for i in range(4):
        sendLeftToRight(rob)
        time.sleep(2)
    '''
    #sendLeftToRight(rob, rob2)
    #rob.close()

    #pickupObjectLeftSide(rob2)
    sendLeftToRight(rob)
    #pickUpFromConveyor(rob)

    rob2.close()
    