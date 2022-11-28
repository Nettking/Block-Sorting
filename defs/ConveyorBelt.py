import time


class ConveyorBelt():

    def __init__(self, robot):
        self.SENSOR_LEFT = 4
        self.SENSOR_RIGHT = 1
        self.robot = robot

    # Conveyor movement control
    def startConveyor(self):
        #start coveyor
        self.robot.set_digital_out(5, 1)
        #allow digital out 5 to stay active for 0.1s
        time.sleep(0.1)
        #set digital out back to 0
        self.robot.set_digital_out(5, 0)
        #conveyor started

    def stopConveyor(self):
        #stop conveyor
        self.robot.set_digital_out(7, 1)
        #allow digital out 7 to stay active for 0.1s
        time.sleep(0.1)
        #set digital out back to 0
        self.robot.set_digital_out(7, 0)
        #conveyor stopped

    def reverseConveyor(self):
        #start coveyor in reverse direction
        self.robot.set_digital_out(6, 1)
        #allow digital out 6 to stay active for 0.1s
        time.sleep(0.1)
        #set digital out back to 0
        self.robot.set_digital_out(6, 0)
        #conveyor started in reverse direction

    def setConveyorSpeed(self, voltage):
        #sets analog out to voltage instead of current
        self.robot.send_program("set_analog_outputdomain(1, 1)")
        #sets analog out 1 to desired voltage. 0.012 is the slowest speed.
        self.robot.set_analog_out(1, voltage)

    def checkSensorReading(self, side):
        sensorReading = None

        if side == self.SENSOR_LEFT:
            sensorReading = self.checkConveyorSensor(self.SENSOR_LEFT)
        elif side == self.SENSOR_RIGHT:
            sensorReading = self.checkConveyorSensor(self.SENSOR_RIGHT)
        
        if sensorReading <= 30:
            self.setConveyorSpeed(0.012)
            self.startConveyor()
            time.sleep(20)
            self.stopConveyor()
   
    def checkConveyorSensor(self, sensor):
        if sensor == self.SENSOR_LEFT: 
            r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[4]/iolinkdevice/pdin"]}})
        if sensor == self.SENSOR_MIDDLE_LEFT: 
            r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[3]/iolinkdevice/pdin"]}})
        if sensor == self.SENSOR_MIDDLE_RIGHT: 
            r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[2]/iolinkdevice/pdin"]}})
        if sensor == self.SENSOR_RIGHT: 
            r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[1]/iolinkdevice/pdin"]}})
        time.sleep(0.1)
        res = r.json()
        res1 = res['data']
        data = str(res1)
        #print(res)

        if data[53] == "2":
            d = data[68]+data[69]
            p = int(d,16)
        else:
            p = ("out of range")
        
        #print('Checking sensor #', sensor, ': ', p)
        if p < int(2):
            print("Object found")
        return p

if __name__ == "__main__":
    belt = ConveyorBelt()
    leftSensorReading = belt.checkSensorReading(belt.SENSOR_LEFT)
    rightSensorReading = belt.checkSensorReading(belt.SENSOR_RIGHT)
    print(f"[LEFT SENSOR READING][{leftSensorReading}]")
    print(f"[RIGHT SENSOR READING][{leftSensorReading}]")

