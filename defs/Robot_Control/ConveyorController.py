import conveyorSensors as cS
import conveyorR2 as conveyor
import time


        
def checkSensorReadingsLeft():         
    # Get sensor data
    sensorLeft = cS.checkConveyorSensor(cS.sensorLeft)

    if sensorLeft <= 30:
        conveyor.setConveyorSpeed(0.012)
        conveyor.startConveyor()
        time.sleep(20)
        conveyor.stopConveyor()
        


def checkSensorReadingsRight():
    # Get sensor data
    sensorRight = cS.checkConveyorSensor(cS.sensorRight)
    
    if sensorRight <= 30:
        if sensorLeft >= 30:
            status = 'Sending right'
            conveyor.setConveyorSpeed(0.012)
            conveyor.reverseConveyor()
            conveyor.time.sleep(20)
            conveyor.stopConveyor()
            

def readRightSide():
    count = 0
    while count < 8:
        count += 1
        checkSensorReadingsRight()
        time.sleep(0.3)

def readLeftSide():
    count = 0
    while count < 2:
        count += 1
        checkSensorReadingsLeft()
        time.sleep(0.3)

#readLeftSide()
#readRightSide()
