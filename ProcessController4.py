

if __name__ == "__main__":

    import time
    import defs.Classes.Robot as Rob
    import defs.Classes.Camera as cam
    import defs.SensorReading as SR
    import urllib.request
    from threading import Thread
    
    stop_threads = False
    stop_threadL = False
    stop_threadR = False
    
    print("Create camera objects.")
    cameraLeft = cam.Camera("10.1.1.8", "left")
    cameraRight = cam.Camera("10.1.1.7", "right")


    def startRobLeft():
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
        time.sleep(2)
        print("Gripper open. Test completed.")
        robotLeft.home()
        time.sleep(2)
        print("Robot Left ready and at home position.")
        return robotLeft
    
    def startRobRight():    
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
        time.sleep(2)
        print("Gripper open. Test completed.")
        robotRight.home()
        time.sleep(2)
        print("Robot Left ready and at home position.")
        robotRight.activateAndOpenGripper()
        time.sleep(1)
        return robotRight
    
    # Connect to robots and conveyor
    robotRight = startRobRight()
    robotLeft = startRobLeft()
    Conveyor = robotRight.robot


#Managing left side 

    def cleanupLeft():
        print("set left cube")
        page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_0')
        time.sleep(3)
        # check for blocks to tidy up on left side 
        
        try:
            x,y = cameraLeft.processRes()
            global stop_threadL, stop_threadR, stop_threads
            global robotLeft
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

            numberOfBlocks = robotRight.sentBlocks
            if robotRight.sentBlocks > 3:
                zPos = 0.20
                numberOfBlocks -= 3
            else:
                zPos = 0.06
            offset = numberOfBlocks*0.06
            block_y_pos = -0.12 - offset
            posDrop = 0.25, block_y_pos, 0.20, 0, 3.14, 0
            
            posDropOff = 0.25, block_y_pos, zPos, 0, 3.14, 0
            robotLeft.move(posDrop)
            robotLeft.move(posDropOff)
            robotLeft.openGripper()
            robotRight.sentBlocks += 1
        except:
            print("No blocks to tidy up on left side")
            stop_threadL = True
            if stop_threadR:
                stop_threads = True


    def sendRight():

        print("set left cylinder")
        page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_1')
        time.sleep(3)
        # Check for blocks to send left to right
        time.sleep(1)
        # Get loc
        try:
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
            numberOfBlocks = robotLeft.sentBlocks
            if robotRight.sentBlocks > 3:
                zPos = 0.20
                numberOfBlocks -= 3
            else:
                zPos = 0.06
            offset = numberOfBlocks*0.06
            block_y_pos = -0.12 - offset
            posDrop = 0.25, block_y_pos, 0.20, 0, 3.14, 0

            #positions x, y, z, rx, ry, rz
            startPosition = 0.25, -0.22, 0.20, 0, 3.14, 0
            pos2 = 0.20, 0.10, 0.30, 0, 3.14, 0
            pos3 = 0.03, 0.30, 0.30, 0, 3.14, 0
            pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
            pos5 = 0.03, 0.30, 0.03, 0, 3.14, 0
            posDropOff = 0.25, block_y_pos, zPos, 0, 3.14, 0
            
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
            robotLeft.sentBlocks += 1
        except:
            print("No blocks to send")



         

################################################################
#right side
    def cleanupRight():
            
        print("set right cylinder")
        page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?sINT_1_1')
        time.sleep(3)
        # check for blocks to tidy up on right side

        # Get loc
        try:
            x,y = cameraRight.processRes()
            time.sleep(1)
            global stop_threads, stop_threadL, stop_threadR
        
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
            numberOfBlocks = robotLeft.sentBlocks
            if robotLeft.sentBlocks > 3:
                zPos = 0.20
                numberOfBlocks -= 3
            else:
                zPos = 0.06
            
            offset = numberOfBlocks*0.1
            block_y_pos = -0.12 - offset
            
            posDrop = 0.25, block_y_pos, 0.20, 0, 3.14, 0
            posDropOff = 0.25, block_y_pos, zPos, 0, 3.14, 0
            robotRight.move(posDrop)
            robotRight.move(posDropOff)
            robotRight.openGripper()
            robotLeft.sentBlocks += 1
        except:
            print("No block to cleanup")
            stop_threadR = True
            if stop_threadL:
                stop_threads = True
    
    def sendLeft():
        print("set right cube")
        page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?sINT_1_0')
        time.sleep(3)
        # Check for blocks to send right to left
        # Get loc
        try:
            x,y = cameraRight.processRes()
            time.sleep(1)
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

            numberOfBlocks = robotRight.sentBlocks
            offset = numberOfBlocks*0.06
            block_y_pos = -0.12 - offset
            posDrop = 0.25, block_y_pos, 0.05, 0, 3.14, 0

            #positions x, y, z, rx, ry, rz
            # creating multiple via positions (pos) to ensure proper robot joint configuration
            startPosition = 0.25, -0.22, 0.20, 0, 3.14, 0
            pos2 = 0.20, 0.10, 0.30, 0, 3.14, 0
            pos3 = 0.03, 0.30, 0.30, 0, 3.14, 0
            pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
            pos5 = 0.03, 0.30, 0.01, 0, 3.14, 0
            #Make sure gripper ready
            robotLeft.openGripper()
            # Move through robot via position
            robotLeft.move(location = startPosition)
            robotLeft.move(location = pos2)
            robotLeft.move(location = pos3)
            robotLeft.move(location = pos4)
            robotLeft.move(location = pos5)
            #Grip block
            robotLeft.closeGripper()
            #Go to home position
            robotLeft.move(location = pos4)
            robotLeft.move(location = pos3)
            robotLeft.move(location = pos2)
            robotLeft.move(location = startPosition)
            #Move to home position
            robotLeft.move(location = posDrop)
            time.sleep(1)
            robotLeft.openGripper()
            time.sleep(2)

            robotLeft.move(location = startPosition)
            time.sleep(5)
            robotLeft.home()
            time.sleep(2)
            robotRight.sentBlocks += 1
        except:
            print("No block found!")



            
if __name__ == "__main__":
    
    def moverob():
        while 1:
            if stop_threads:
                break
            cleanupLeft()
    def moverob2():
        while 1:
            if stop_threads:
                break
            cleanupRight()
    
    # Starting cleanup threads (both robots clean at the same time)
    Thread(method = moverob).start()
    Thread(method = moverob2).start()
    print("Waiting up to 300 for cleanup to complete")
    counter = 0
    while counter < 300:
        counter+=1
        if stop_threads == True:
            time.sleep(1)
            sendLeft()
            sendRight()
            break
        else:
            time.sleep(1)
    
    # starting cleanup checkup after initial cleanup
    while True:
        cleanupLeft()
        cleanupRight()
        sendLeft()
        sendRight()
