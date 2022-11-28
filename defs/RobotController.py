import time
from Gripper import *
import ConveyorController as CC
import Classes.Camera as cam
import Classes.Robot as robot


sentBlocks = 0
pos_multiplyer = 0.06
block_y_pos = -0.22 - (sentBlocks*pos_multiplyer)

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

def pickUpFromConveyor(rob):
    global block_y_pos

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
    move(rob, pos1)
    move(rob, pos6)
    move(rob, pos7)

    rob.send_program(rq_open())
    time.sleep(2)

    move(rob, pos6)
    move(rob, pos1)

    
def getImputFromLeftCamera():
    print("[GETTING X,Y FROM LEFT CAMERA]")
    x,y = cam.resultCameraLeft
    return x,y
    
    '''
    x, y = camera.checkForBlock()
    print("[VALIDATING X AND Y]")
    if (x == None or y == None):
        x, y = camera.checkForBlock()
    return x, y
'''


def setPositionFromCameraInputLeft():
    x,y = getImputFromLeftCamera()
    print(f"[POST VALIDATION X AND Y][X = {x}, Y = {y}]")
    # Left side has reversed y-value 
    positionPickUp = (x,-y,0.20,0.05,3.14,0)
    #positionPickUpDown = (x,y,0.15,0,3.14,0)
    return positionPickUp

def sendLeftToRight(rob):
    positionPickUp = setPositionFromCameraInputLeft()
    
    print("[MOVING ROBOT]")    
    move(rob, positionPickUp)
    rob2.send_program(rq_close())
    time.sleep(3)


'''
    print("[FINISHED MOVING ROBOT 2]")
    time.sleep(3)
    sensorvalue = 0
    CC.checkSensorReadingsLeft()
    time.sleep(2)
    print("DONE CHECKING SENSORS")
    if sensorValue != 0 or sensorValue != None:
        print("INSIDE IF")
        pickUpFromConveyor(rob)
        global sentBlocks, block_y_pos 
        sentBlocks += 1
        block_y_pos = -0.22 - (sentBlocks*pos_multiplyer)

    print("DONE WITH sendLeftToRight")
'''

def sendRightToLeft():
    #sensorLeft = CC.checkSensorReadingsLeft()
    return

    

def pickupObjectLeftSide(rob):

    positionPickUp = setPositionFromCameraInputLeft()

    print(positionPickUp)
    
    print("[MOVING ROBOT 2]")
    move(rob, positionPickUp)

    rob.send_program(rq_close())
    time.sleep(3)

    print("[FINISHED MOVING ROBOT 2]")
    time.sleep(3)




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
    