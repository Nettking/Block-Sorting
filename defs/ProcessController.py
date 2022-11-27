import RobotController as RC
import Classes.Camera as cam
import time

def initialize():
    ################################################################
    #                         Starte roboter                       #
    ################################################################
    # Initialisere roboter:
    ## For begge robotarmene:
    ## Opprett tilkobling
    robLeft = RC.rob
    robRight = RC.rob2
    
    ## Aktiver og åpne kloer
    RC.activateAndOpenGripper(robLeft)
    RC.activateAndOpenGripper(robRight)

    ## Sett TCP
    robLeft.set_tcp(0,0,0.16,0,0,0)
    time.sleep(0.3)
    robLeft.set_tcp(0,0,0.16,0,0,0)
    time.sleep(0.3)

    ## Gå til hjemposisjon ( Denne må oppdateres )
    homePositionLeft = 0.03, 0.03, 0.3, 0, 3.14, 0
    homePositionRight = 0.03, 0.03, 0.3, 0, 3.14, 0
    RC.move(robLeft, homePositionLeft)
    time.sleep(5)
    RC.move(robRight, homePositionRight)
    time.sleep(5)
    
    # Opprett tilkobling til begge kameraene
    cameraLeft = cam.cameraLeft
    cameraRight = cam.cameraRight


def controlLeftSide():
    # Sjekk venstre side for blokker
    resultCameraLeft = cam.resultCameraLeft 

    ## Hvis Blokker funnet: Flytt blokk, sjekk kamera på nytt
    ### Finn posisjon blokk
    ### Gå til blokk
    ### Plukk opp blokk
    ### Sett blokk på beltet
    ### Kjør blokk til andre siden  
    ### Plukk av blokk og plasser.
    if len(resultCameraLeft)> 2: # Blokk funnet
        RC.sendLeftToRight()
        time.sleep(1)
        controlLeftSide()
    elif len(resultCameraLeft)< 2:
        time.sleep(1) ## Hvis ikke blokker funnet: Bytt kamera etter 1 sec
    return

def controlRightSide():
    # Sjekk høyre side for blokker
    resultCameraRight = cam.resultCameraRight 

    ## Hvis Blokker funnet: Flytt blokk, sjekk kamera på nytt
    ### Finn posisjon blokk
    ### Gå til blokk
    ### Plukk opp blokk
    ### Sett blokk på beltet
    ### Kjør blokk til andre siden  
    ### Plukk av blokk og plasser.
    if len(resultCameraRight)> 2: # Blokk funnet
        RC.sendLeftToRight()
        time.sleep(1)
        controlLeftSide()
    elif len(resultCameraRight)< 2:
        time.sleep(1) ## Hvis ikke blokker funnet: Bytt kamera etter 1 sec
    return

def main():
 
    ################################################################
    #                       Se etter blokker                       #
    ################################################################
    # Sjekk venstre side for blokker - flytt alle til høyre
    controlLeftSide()

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
    main()