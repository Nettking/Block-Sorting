

if __name__ == "__main__":
    import time
    import defs.Classes.Robot as Rob
    import defs.Classes.Camera as cam
    print("CREATING ROBOT OBJECCT")
    robotLeft = Rob.Robot("10.1.1.6", (0.25, -0.22, 0.20, 0, 3.14, 0) )
    robotRight = Rob.Robot("10.1.1.5", (0.25, -0.22, 0.20, 0, 3.14, 0) ) 
    
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
    
    x,y = cameraLeft.processRes()
    pos = x,-y,0.1,0,3.14,0
    robotLeft.move(pos)
    robotRight.close()
    robotLeft.close()



