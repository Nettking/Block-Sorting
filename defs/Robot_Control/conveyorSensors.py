import requests
import asyncio
import time


sensorLeft = 4
sensorMiddleLeft = 3
sensorMiddleRight = 2
sensorRight = 1

def checkConveyorSensor(sensor):
    if sensor == sensorLeft: 
        r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[4]/iolinkdevice/pdin"]}})
    if sensor == sensorMiddleLeft: 
        r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[3]/iolinkdevice/pdin"]}})
    if sensor == sensorMiddleRight: 
        r = requests.post('http://10.1.1.9', json={"code":"request","cid":1,"adr":"/getdatamulti","data":{"datatosend":["/iolinkmaster/port[2]/iolinkdevice/pdin"]}})
    if sensor == sensorRight: 
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
    
    print('Checking sensor #', sensor, ': ', p)
    if p < int(2):
        print("Object found")
    return p





def checkConveyorSensors():
    checkConveyorSensor(sensorLeft)
    checkConveyorSensor(sensorMiddleLeft)
    checkConveyorSensor(sensorMiddleRight)
    checkConveyorSensor(sensorRight)

