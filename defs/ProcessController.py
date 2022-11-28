import RobotController as RC
import Classes.Camera as cam
import time
import urx


def initialize():
    ################################################################
    #                         Starte roboter                       #
    ################################################################
    # Initialisere roboter:
    ## For begge robotarmene:
    ## Opprett tilkobling
    #set robot ip adresses
    r1="10.1.1.6"
    r2="10.1.1.5"

    robLeft = urx.Robot(r1, use_rt=True, urFirm=5.1)
    robRight = urx.Robot(r2, use_rt=True, urFirm=5.1)


    try:
        robLeft = urx.Robot(r1, use_rt=True, urFirm=5.1)#RC.rob
        time.sleep(0.3)
    except:
        print("Failed to initialize robot #1")

    try:    
        robRight = urx.Robot(r2, use_rt=True, urFirm=5.1)#RC.rob2
        time.sleep(0.3)
    except:
        print("Failed to initialize robot #2")

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
    
    ## Sett TCP
    try:
        robLeft.set_tcp(0,0,0.16,0,0,0)
        time.sleep(0.3)
    except:
        print("Failed to set TCP on robot #1")
    
    try:
        robRight.set_tcp(0,0,0.16,0,0,0)
        time.sleep(0.3)
    except:
        print("Failed to set TCP on robot #2")
    
    ## Gå til hjemposisjon ( Denne må oppdateres )
    homePositionLeft = 0.25, -0.22, 0.20, 0, 3.14, 0
    homePositionRight = 0.25, -0.22, 0.20, 0, 3.14, 0
    try:
        RC.move(robLeft, homePositionLeft)
        time.sleep(5)
    except:
        print("Failed to move robot to homePositionLeft")
    
    try:
        RC.move(robRight, homePositionRight)
        time.sleep(5)
    except:
        print("Failed to move robot to homePositionRight")
    
    # Opprett tilkobling til begge kameraene
    try: 
        cameraLeft = cam.cameraLeft
    except:
        print("Failed to initialize camera #1")
    try:
        cameraRight = cam.cameraRight
    except:
        print("Failed to initialize camera #2")


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


# Starte opp roboter
initialize()

# Sjekk 100 ganger for blokker
count = 0
while count < 100:
    count += 1
    try:
        main()
    except:
        print("Exception has been thrown by main loop")
        