import Robot_Control.SensorReading as SR
import time
import Classes.Robot as Robot

#Access robot connected to conveyor
rob2 = Robot.robRight





def startConveyor():
    #start coveyor
    rob2.set_digital_out(5, 1)
    #allow digital out 5 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    rob2.set_digital_out(5, 0)
    #conveyor started

def stopConveyor():
    #stop conveyor
    rob2.set_digital_out(7, 1)
    #allow digital out 7 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    rob2.set_digital_out(7, 0)
    #conveyor stopped

def reverseConveyor():
    #start coveyor in reverse direction
    rob2.set_digital_out(6, 1)
    #allow digital out 6 to stay active for 0.1s
    time.sleep(0.1)
    #set digital out back to 0
    rob2.set_digital_out(6, 0)
    #conveyor started in reverse direction

def setConveyorSpeed(voltage):
    #sets analog out to voltage instead of current
    rob2.send_program("set_analog_outputdomain(1, 1)")
    #sets analog out 1 to desired voltage. 0.012 is the slowest speed.
    rob2.set_analog_out(1, voltage)





        
def checkSensorReadingsLeft():         
    # Get sensor data
    sensorLeft = SR.checkConveyorSensor(SR.sensorLeft)
    
    # If block found start conveyor belt
    if sensorLeft <= 30:
        setConveyorSpeed(0.012)
        startConveyor()
        time.sleep(20)
        stopConveyor()
        


def checkSensorReadingsRight():
    # Get sensor data
    sensorRight = SR.checkConveyorSensor(SR.sensorRight)
    
    # If block found start conveyor belt
    if sensorRight <= 30:
        setConveyorSpeed(0.012)
        reverseConveyor()
        time.sleep(20)
        stopConveyor()


checkSensorReadingsLeft()

