import SensorReading as SR
import defs.Classes.Conveyor as conveyor
import time

        
def checkSensorReadingsLeft():         
    # Get sensor data
    sensorLeft = SR.checkConveyorSensor(SR.sensorLeft)
    

    if sensorLeft <= 30:
        conveyor.setConveyorSpeed(0.012)
        conveyor.startConveyor()
        time.sleep(20)
        conveyor.stopConveyor()
        


def checkSensorReadingsRight():
    # Get sensor data
    sensorRight = SR.checkConveyorSensor(SR.sensorRight)
    
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
