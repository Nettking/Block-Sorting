

if __name__ == "__main__":

    import time
    import defs.Classes.Robot as Rob
    import defs.Classes.Camera as cam
    #from defs.Classes.ConveyorBelt import ConveyorBelt
    #import defs.ConveyorController as CC
    import defs.SensorReading as SR
    import urx

        
    print("CREATING ROBOT OBJECCT")

    r2="10.1.1.5"

    #Belt = ConveyorBelt(robotRight)
    robotLeft = Rob.Robot("10.1.1.6", (0.25, -0.22, 0.20, 0, 3.14, 0) )
    robotLeft.initRobot()
    time.sleep(1)
    robotLeft.setTCP( (0,0,0.16,0,0,0) )
    time.sleep(1)
    robotLeft.activateAndOpenGripper()

    time.sleep(1)
    robotLeft.closeGripper()
    time.sleep(1)
    robotLeft.openGripper()
    time.sleep(5)
    robotLeft.home()

    cameraLeft = cam.Camera("10.1.1.8", "left")
    
    count = 0
    while count < 3:
        rob2 = urx.Robot(r2, use_rt=True, urFirm=5.1)
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
        #Belt.checkSensorReading(1)
        sensorLeft = SR.checkConveyorSensor(SR.sensorLeft)
        time.sleep(2)
        # If block found start conveyor belt
        print(sensorLeft)
        rob2.set_digital_out(5, 1)
        #allow digital out 5 to stay active for 0.1s
        time.sleep(0.1)
        #set digital out back to 0
        rob2.set_digital_out(5, 0)
        time.sleep(21)
        rob2.set_digital_out(7, 1)
        #allow digital out 5 to stay active for 0.1s
        time.sleep(0.1)
        #set digital out back to 0
        rob2.set_digital_out(7, 0)
        time.sleep(1)
        rob2.close()
        time.sleep(5)
        robotRight = Rob.Robot("10.1.1.5", 1)
        time.sleep(1)
        robotRight.initRobot()
        time.sleep(2)
        tcp = 0,0,0,0,0,0
        robotRight.setTCP(tcp)
        time.sleep(1)

        robotRight.activateAndOpenGripper()
        time.sleep(1)
        robotRight.home()
        time.sleep(2)
        numberOfBlocks = float(count-1)
        offset = numberOfBlocks*0.06
        block_y_pos = -0,22 - offset
        posDrop = 0.25, block_y_pos, 0.20, 0, 3.14, 0

        #positions x, y, z, rx, ry, rz
        startPosition = 0.25, -0.22, 0.20, 0, 3.14, 0
        pos2 = 0.20, 0.10, 0.30, 0, 3.14, 0
        pos3 = 0.03, 0.30, 0.30, 0, 3.14, 0
        pos4 = 0.03, 0.30, 0.25, 0, 3.14, 0
        pos5 = 0.03, 0.30, 0.15, 0, 3.14, 0
        pos6 = 0.25, block_y_pos, 0.20, 0, 3.14, 0
        #pos7 = 0.25, block_y_pos, 0.20, 0, 3.14, 0

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
        #robotRight.move(location = pos7)

        robotRight.openGripper()
        time.sleep(2)

        robotRight.move(location = startPosition)
        time.sleep(5)
        robotRight.home()
        time.sleep(2)
        robotRight.close()
        time.sleep(2)
