

if __name__ == "__main__":

    import time
    import defs.Classes.Robot as Rob
    import defs.Classes.Camera as cam
    #from defs.Classes.ConveyorBelt import ConveyorBelt
    #import defs.ConveyorController as CC
    import defs.SensorReading as SR
    import urx
    import urllib.request

    robotLeft = Rob.Robot("10.1.1.6", (0.25, -0.22, 0.20, 0, 3.14, 0) )
    time.sleep(1)
    robotLeft.initRobot()
    time.sleep(2)
    print("Robot Left initialized.")
    robotLeft.setTCP( (0,0,0.16,0,0,0) )
    time.sleep(1)
    print("Robot Left TCP set.")
    robotLeft.activateAndOpenGripper()
    time.sleep(1)
    print("Gripper activated. Testing gripper")
    robotLeft.closeGripper()
    time.sleep(1)
    print("Gripper closed.")
    robotLeft.openGripper()
    time.sleep(5)
    print("Gripper open. Test completed.")
    robotLeft.home()
    time.sleep(2)
    print("Robot Left ready and at home position.")
    
    robotRight = Rob.Robot("10.1.1.5", 1)
    time.sleep(1)
    robotRight.initRobot()
    print("Robot Right initialized.")
    time.sleep(2)
    tcp = 0,0,0.16,0,0,0
    robotRight.setTCP(tcp)
    time.sleep(1)
    print("Robot Left TCP set.")
    robotRight.activateAndOpenGripper()
    time.sleep(1)
    print("Gripper activated. Testing gripper")
    robotRight.closeGripper()
    time.sleep(1)
    print("Gripper closed.")
    robotRight.openGripper()
    time.sleep(5)
    print("Gripper open. Test completed.")
    robotRight.home()
    time.sleep(2)
    print("Robot Left ready and at home position.")
    robotRight.activateAndOpenGripper()
    time.sleep(1)

    Conveyor = robotRight.robot


    print("Create camera objects.")
    cameraLeft = cam.Camera("10.1.1.8", "left")
    cameraRight = cam.Camera("10.1.1.7", "right")
    count = 0
    tidyL = 0


    print("set left cube")
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_0')
    time.sleep(3)
    # check for blocks to tidy up on left side
    
    while count < 2:
        count += 1
        # Get loc
        x,y = cameraLeft.processRes()
        if x:
            overBlock = x,y,0.1,0,3.14,0
            # Move over loc
            robotLeft.move(overBlock)
            blockPickUpPos = x,y,0.03,0,3.14,0
            # Move down to block
            robotLeft.move(blockPickUpPos)
            robotLeft.closeGripper()
            
            time.sleep(2)
            # Move up
            robotLeft.move(overBlock)
            # Move home
            robotLeft.home()

            numberOfBlocks = count-1
            offset = numberOfBlocks*0.06
            block_y_pos = -0.12 - offset
            posDrop = 0.25, block_y_pos, 0.20, 0, 3.14, 0
            
            posDropOff = 0.25, block_y_pos, 0.04, 0, 3.14, 0
            robotLeft.move(posDrop)
            robotLeft.move(posDropOff)
            robotLeft.openGripper()
            tidyL += 1
        else:
            break



    print("set left cylinder")
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_1')
    time.sleep(3)
    count = 0
    l2r = 0
    # Check for blocks to send left to right
    while count < 1:
        time.sleep(1)
        count += 1
        # Get loc
        x,y = cameraLeft.processRes()
         
    overBlock = x,y,0.1,0,3.14,0
    # Move over loc
    robotLeft.move(overBlock)
    blockPickUpPos = x,y,0.03,0,3.14,0
    # Move down to block
    robotLeft.move(blockPickUpPos)
    robotLeft.closeGripper()
    time.sleep(2)
    # Move up
    robotLeft.move(overBlock)
    # Move home
    robotLeft.home()
    robotLeft.placeOnConveyor()
    time.sleep(2)
    sensorLeft = SR.checkConveyorSensor(SR.sensorLeft)
    time.sleep(2)
    # If block found start conveyor belt
    print(sensorLeft)
    Conveyor.set_digital_out(5, 1)
    #allow digital out 5 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    Conveyor.set_digital_out(5, 0)
    time.sleep(21)
    Conveyor.set_digital_out(7, 1)
    #allow digital out 5 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    Conveyor.set_digital_out(7, 0)
    time.sleep(1)

    # Block on right side
    numberOfBlocks = float(count-1+l2r)
    offset = numberOfBlocks*0.06
    block_y_pos = -0.12 - offset
    posDrop = 0.25, block_y_pos, 0.20, 0, 3.14, 0

    #positions x, y, z, rx, ry, rz
    startPosition = 0.25, -0.22, 0.20, 0, 3.14, 0
    pos2 = 0.20, 0.10, 0.30, 0, 3.14, 0
    pos3 = 0.03, 0.30, 0.30, 0, 3.14, 0
    pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
    pos5 = 0.03, 0.30, 0.03, 0, 3.14, 0
    pos6 = 0.25, block_y_pos, 0.20, 0, 3.14, 0
    #pos7 = 0.25, block_y_pos, 0.20, 0, 3.14, 0
    posDropOff = 0.25, block_y_pos, 0.04, 0, 3.14, 0
    robotRight.openGripper()

    robotRight.move(location = startPosition)
    robotRight.move(location = pos2)
    robotRight.move(location = pos3)
    robotRight.move(location = pos4)
    robotRight.move(location = pos5)
    
    robotRight.closeGripper()

    robotRight.move(location = pos4)
    robotRight.move(location = pos3)
    robotRight.move(location = pos2)
    robotRight.move(location = startPosition)
    time.sleep(1)
    robotRight.move(location = posDrop)
    robotRight.move(posDropOff)
    robotRight.openGripper()
    time.sleep(2)

    robotRight.move(location = startPosition)
    time.sleep(5)
    robotRight.home()
    time.sleep(2)
    l2r += 1




         

################################################################
#right side
    print("set right cylinder")
    page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?sINT_1_1')
    time.sleep(3)
    count = 0
 # check for blocks to tidy up on right side
    while count < 2:
        count += 1
        # Get loc
        x,y = cameraRight.processRes()
        if x:
            overBlock = x,y,0.1,0,3.14,0
            # Move over loc
            robotRight.move(overBlock)
            blockPickUpPos = x,y,0.03,0,3.14,0
            # Move down to block
            robotRight.move(blockPickUpPos)
            robotRight.closeGripper()
            time.sleep(2)
            # Move up
            robotRight.move(overBlock)
            # Move home
            robotRight.home()

            numberOfBlocks = count-1+l2r
            offset = numberOfBlocks*0.1
            block_y_pos = -0.12 - offset
            posDrop = 0.25, block_y_pos, 0.20, 0, 3.14, 0
            posDropOff = 0.25, block_y_pos, 0.06, 0, 3.14, 0
            robotRight.move(posDrop)
            robotRight.move(posDropOff)
            robotRight.openGripper()
        else:
            break

    print("set right cube")
    page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?sINT_1_0')
    time.sleep(3)
    # Check for blocks to send right to left
    count = 0
    while count < 1:
        time.sleep(1)
        count += 1
        # Get loc
        x,y = cameraRight.processRes()
        if x: 
            overBlock = x,y,0.1,0,3.14,0
            # Move over loc
            robotRight.move(overBlock)
            blockPickUpPos = x,y,0.03,0,3.14,0
            # Move down to block
            robotRight.move(blockPickUpPos)
            robotRight.closeGripper()
            time.sleep(2)
            # Move up
            robotRight.move(overBlock)
            # Move home
            robotRight.home()
            robotRight.placeOnConveyor()
            #Belt.checkSensorReading(1)
            time.sleep(2)
            sensorRight = SR.checkConveyorSensor(SR.sensorLeft)
            time.sleep(2)
            # If block found start conveyor belt
            print(sensorRight)
            Conveyor.set_digital_out(6, 1)
            #allow digital out 5 to stay active for 0.1s
            time.sleep(0.1)
            #set digital out back to 0
            Conveyor.set_digital_out(6, 0)
            time.sleep(20.5)
            Conveyor.set_digital_out(7, 1)
            #allow digital out 5 to stay active for 0.1s
            time.sleep(0.1)
            #set digital out back to 0
            Conveyor.set_digital_out(7, 0)
            time.sleep(1)

            numberOfBlocks = float(count+l2r)
            offset = numberOfBlocks*0.06
            block_y_pos = -0.12 - offset
            posDrop = 0.25, block_y_pos, 0.05, 0, 3.14, 0

            #positions x, y, z, rx, ry, rz
            startPosition = 0.25, -0.22, 0.20, 0, 3.14, 0
            pos2 = 0.20, 0.10, 0.30, 0, 3.14, 0
            pos3 = 0.03, 0.30, 0.30, 0, 3.14, 0
            pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
            pos5 = 0.03, 0.30, 0.01, 0, 3.14, 0
            pos6 = 0.25, block_y_pos, 0.20, 0, 3.14, 0
            #pos7 = 0.25, block_y_pos, 0.20, 0, 3.14, 0

            robotLeft.openGripper()

            robotLeft.move(location = startPosition)
            robotLeft.move(location = pos2)
            robotLeft.move(location = pos3)
            robotLeft.move(location = pos4)
            robotLeft.move(location = pos5)
            
            robotLeft.closeGripper()

            robotLeft.move(location = pos4)
            robotLeft.move(location = pos3)
            robotLeft.move(location = pos2)
            robotLeft.move(location = startPosition)
            
            robotLeft.move(location = posDrop)
            time.sleep(1)
            robotLeft.openGripper()
            time.sleep(2)

            robotLeft.move(location = startPosition)
            time.sleep(5)
            robotLeft.home()
            time.sleep(2)
        else:
            break



         


