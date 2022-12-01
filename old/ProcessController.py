import time
from Robot import Robot
from Camera import Camera
from ConveyorBelt import ConveyorBelt

def initialize(rob: Robot, rob2: Robot):
    try:
        rob.initRobot()
        rob.setTCP()
        rob.activateAndOpenGripper()
        rob.home()
        time.sleep(2)
        rob2.initRobot()
        rob2.setTCP()
        rob2.activateAndOpenGripper()
        rob2.home()
        return True
    except:
        return False
    
def send(robotSend: Robot, robotPickup: Robot, belt: ConveyorBelt):
    robotSend.pickupFromWorkspace()
    robotSend.placeOnConveyor()
    if robotSend.side == belt.SENSOR_LEFT:
        belt.checkSensorReading(belt.SENSOR_LEFT)
    else:
        belt.checkSensorReading(belt.SENSOR_RIGHT)
    robotPickup.pickUpFromConveyor()

def controlLeftSide(resultCameraLeft, robotLeft, robotRight, belt):
    ## Hvis Blokker funnet: Flytt blokk, sjekk kamera på nytt
    ### Finn posisjon blokk
    ### Gå til blokk
    ### Plukk opp blokk
    ### Sett blokk på beltet
    ### Kjør blokk til andre siden  
    ### Plukk av blokk og plasser.
    if len(resultCameraLeft)> 2: # Blokk funnet
        send(robotLeft, robotRight, belt)
        time.sleep(1)
        #controlLeftSide()
    elif len(resultCameraLeft)< 2:
        time.sleep(1) ## Hvis ikke blokker funnet: Bytt kamera etter 1 sec

def controlRightSide(resultCameraRight, robotLeft, robotRight, belt):
    ## Hvis Blokker funnet: Flytt blokk, sjekk kamera på nytt
    ### Finn posisjon blokk
    ### Gå til blokk
    ### Plukk opp blokk
    ### Sett blokk på beltet
    ### Kjør blokk til andre siden  
    ### Plukk av blokk og plasser.
    if len(resultCameraRight)> 2: # Blokk funnet
        send(robotRight, robotLeft, belt)
        time.sleep(1)
        #controlRightSide()
    elif len(resultCameraRight)< 2:
        time.sleep(1) ## Hvis ikke blokker funnet: Bytt kamera etter 1 sec

def main(resultCameraLeft, resultCameraRight, robotLeft, robotRight, belt):
 
    ################################################################
    #                       Se etter blokker                       #
    ################################################################
    # Sjekk venstre side for blokker - flytt alle til høyre
    controlLeftSide(resultCameraLeft, robotLeft, robotRight, belt)

    ## Hvis ikke blokker funnet: Bytt kamera

    # Sjekk høyre side for blokker - - flytt alle til venstre
    controlRightSide(resultCameraRight, robotLeft, robotRight, belt)    
    
    ## Hvis ikke blokker funnet: Bytt kamera

    # Vent 1 sekund
    time.sleep(1)


if __name__ == "__main__":
    maxInitTries = 0

    cameraLeft = Camera("10.1.1.8")
    cameraRight = Camera("10.1.1.7")

    robotLeft = Robot("10.1.1.5")
    robotRight = Robot("10.1.1.6")

    belt = ConveyorBelt(robotRight)

    isInitialized = False
    isInitialized = initialize()
    if isInitialized:
        # Sjekk 100 ganger for blokker
        count = 0
        while count < 100:
            count += 1
            try:
                resultCameraLeft = cameraLeft.setPositionFromCameraInput()
                resultCameraRight = cameraRight.setPositionFromCameraInput()
                main(resultCameraLeft, resultCameraRight, belt)
            except:
                print("Exception has been thrown by main loop")
    elif maxInitTries < 10:
        print("Failed to initialize")
        maxInitTries += 1
        isInitialized = initialize()