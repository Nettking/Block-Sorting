import RobotController as RC
import Classes.Camera as cam
import time
import urx

r_ip="10.1.1.6"
l_ip="10.1.1.5"
robLeft = None
robRight = None
maxInitTries = 0

def initialize():
    ################################################################
    #                         Starte roboter                       #
    ################################################################
    # Initialisere roboter:
    ## For begge robotarmene:
    ## Opprett tilkobling
    #set robot ip adresses
    global r_ip, l_ip
    isRobRightInit = initRobotRight(r_ip)
    isRobLeftInit = initRobotLeft(l_ip)

    if isRobRightInit and isRobLeftInit:
        initGrippers()
        isTCPLeftSet = setTCPLeft()
        isTCPRightSet = setTCPRight()

        if isTCPLeftSet and isTCPRightSet:
            isRobotLeftHomed = homeRobotLeft()
            isRobotRightHomed = homeRobotRight()

            if isRobotLeftHomed and isRobotRightHomed:
                isCameraLeftInit = initCameraLeft()
                isCameraRightInit = initCameraRight()
                
                if isCameraLeftInit and isCameraRightInit:
                    return True
                else:
                    return False
    
    return False

# Opprett tilkobling til begge kameraene
def initCameraLeft():
    try: 
        cameraLeft = cam.cameraLeft
    except:
        print("Failed to initialize camera #1")

def initCameraRight():
    try:
        cameraRight = cam.cameraRight
    except:
        print("Failed to initialize camera #2")
def initRobotLeft(rob_ip):
    try:
        global robLeft, isRobLeftInit
        robLeft = urx.Robot(rob_ip, use_rt=True, urFirm=5.1)#RC.rob
        time.sleep(0.3)
        return True
    except:
        print("Failed to initialize robot #1")
        return False

def initRobotRight(rob_ip):
    try:
        global robRight, isRobRightInit    
        robRight = urx.Robot(rob_ip, use_rt=True, urFirm=5.1)#RC.rob2
        time.sleep(0.3)
        return True
    except:
        print("Failed to initialize robot #2")
        return False

def initGrippers():
    ## Aktiver og åpne kloer
    try:
        RC.activateAndOpenGripper(robLeft)
        time.sleep(0.3)
    except:
        print("Failed to activate and open gripper #1")
    
    try:
        RC.activateAndOpenGripper(robRight)
        time.sleep(0.3)
    except:
        print("Failed to activate and open gripper #2")

def initCameras():
    pass

def setTCPLeft():
    ## Sett TCP
    try:
        robLeft.set_tcp(0,0,0.16,0,0,0)
        time.sleep(0.3)
        return True
    except:
        print("Failed to set TCP on robot #1")
        return False
    

def setTCPRight():
    try:
        robRight.set_tcp(0,0,0.16,0,0,0)
        time.sleep(0.3)
        return True
    except:
        print("Failed to set TCP on robot #2")
        return False

def homeRobotLeft():
    ## Gå til hjemposisjon ( Denne må oppdateres )
    homePositionLeft = 0.25, -0.22, 0.20, 0, 3.14, 0
    try:
        RC.move(robLeft, homePositionLeft)
        time.sleep(5)
        return True
    except:
        print("Failed to move robot to homePositionLeft")
        return False
        
def homeRobotRight():
    homePositionRight = 0.25, -0.22, 0.20, 0, 3.14, 0
    try:
        RC.move(robRight, homePositionRight)
        time.sleep(5)
        return True
    except:
        print("Failed to move robot to homePositionRight")
        return False

def controlLeftSide():
    # Sjekk venstre side for blokker
    try:
        resultCameraLeft = cam.resultCameraLeft 
    except:
        print("Failed to get results from camera #1")
    ## Hvis Blokker funnet: Flytt blokk, sjekk kamera på nytt
    ### Finn posisjon blokk
    ### Gå til blokk
    ### Plukk opp blokk
    ### Sett blokk på beltet
    ### Kjør blokk til andre siden  
    ### Plukk av blokk og plasser.
    try:
        if len(resultCameraLeft)> 2: # Blokk funnet
            RC.sendLeftToRight()
            time.sleep(1)
            #controlLeftSide()
        elif len(resultCameraLeft)< 2:
            time.sleep(1) ## Hvis ikke blokker funnet: Bytt kamera etter 1 sec
        return
    except:
        print("Failed to control left side")

def controlRightSide():
    # Sjekk høyre side for blokker
    try:
        resultCameraRight = cam.resultCameraRight 
    except:
        print("Failed to get results from camera #2")
    ## Hvis Blokker funnet: Flytt blokk, sjekk kamera på nytt
    ### Finn posisjon blokk
    ### Gå til blokk
    ### Plukk opp blokk
    ### Sett blokk på beltet
    ### Kjør blokk til andre siden  
    ### Plukk av blokk og plasser.
    try:
        if len(resultCameraRight)> 2: # Blokk funnet
            RC.sendLeftToRight()
            time.sleep(1)
            #controlRightSide()
        elif len(resultCameraRight)< 2:
            time.sleep(1) ## Hvis ikke blokker funnet: Bytt kamera etter 1 sec
        return
    except:
        print("Failed to control right side")


def main():
 
    ################################################################
    #                       Se etter blokker                       #
    ################################################################
    # Sjekk venstre side for blokker - flytt alle til høyre
    controlLeftSide()

    ## Hvis ikke blokker funnet: Bytt kamera

    # Sjekk høyre side for blokker - - flytt alle til venstre
    controlRightSide()    
    
    ## Hvis ikke blokker funnet: Bytt kamera

    # Vent 1 sekund
    time.sleep(1)


if __name__ == "__main__":
    # Starte opp roboter
    isInitialized = initialize()

    if isInitialized:
        # Sjekk 100 ganger for blokker
        count = 0
        while count < 100:
            count += 1
            try:
                main()
            except:
                print("Exception has been thrown by main loop")
    elif maxInitTries < 10:
        print("Failed to initialize")
        maxInitTries += 1
        isInitialized = initialize()