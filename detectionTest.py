

if __name__ == "__main__":
    import time
    import defs.Classes.Robot as Rob
    import defs.Classes.Camera as cam
    from defs.Classes.ConveyorBelt import ConveyorBelt
    

   
    print("CREATING ROBOT OBJECCT")
    robotLeft = Rob.Robot("10.1.1.6", (0.25, -0.22, 0.20, 0, 3.14, 0) )
    robotRight = Rob.Robot("10.1.1.5", (0.25, -0.22, 0.20, 0, 3.14, 0) ) 
    robotRight.initRobot()
    time.sleep(2)
    robotRight.home()
    Belt = ConveyorBelt(robotRight)
    robotLeft.initRobot()
    robotLeft.setTCP( (0,0,0.16,0,0,0) )
    time.sleep(3)
    robotLeft.activateAndOpenGripper()

    time.sleep(2)
    robotLeft.closeGripper()
    robotLeft.openGripper()
    time.sleep(2)
    robotLeft.home()

    cameraLeft = cam.Camera("10.1.1.8", "left")
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
    Belt.checkSensorReading(1)
    robotRight.pickUpFromConveyor()

    robotRight.close()
    robotLeft.close()



