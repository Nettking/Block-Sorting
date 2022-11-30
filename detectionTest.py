

if __name__ == "__main__":
    import time
    import defs.Classes.Robot as Rob
    import defs.Classes.Camera as cam
    #from defs.Classes.ConveyorBelt import ConveyorBelt
    #import defs.ConveyorController as CC
    import defs.SensorReading as SR
    import urx

    r2="10.1.1.5"
    rob2 = urx.Robot(r2, use_rt=True, urFirm=5.1)
    print("CREATING ROBOT OBJECCT")
    
    robotRight = Rob.Robot("10.1.1.5", (0.25, -0.22, 0.20, 0, 3.14, 0) ) 
    robotRight.initRobot()
    #Belt = ConveyorBelt(robotRight)
    robotLeft.initRobot()
    time.sleep(1)
    robotLeft.setTCP( (0,0,0.16,0,0,0) )
    time.sleep(1)
    robotLeft.activateAndOpenGripper()

    time.sleep(1)
    robotLeft.closeGripper()
    time.sleep(1)
    robotLeft.openGripper()
    time.sleep(1)
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
    #Belt.checkSensorReading(1)
    sensorLeft = SR.checkConveyorSensor(SR.sensorLeft)
    time.sleep(2)
    # If block found start conveyor belt
    print(sensorLeft)
    robotRight.
