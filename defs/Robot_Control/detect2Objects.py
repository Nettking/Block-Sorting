import urx
import urllib.request
import time
x = float(25/1000)
y = float(-385/1000)
lasty = y
lastx = x
objectLocated = 0
whichObject = 0
switchCounter = 0


def handleCameraOutput(side, page):
    #reads output from camera
    coords = page.read().decode('utf-8')
    #splits output
    x1 = coords.split(",")
    whichObject = int(x1[1])
    objectLocated = int(x1[2])
    # check if no block
    if len(x1) < 2:
        # No block found
        handleCameraOutput(side, page)
    else:
        # NO. Blocks > 0
        if objectLocated == 1:
            switchCounter = 0
            y = x1[4]
            x = x1[3]
            x = (float(x) + 25) /1000
            y = (float(y) - 385) /1000
            time.sleep(3)
            print(x, y)
            if side == "left": 
                locateObjectsLeft()
            if side == "right": 
                locateObjectsRight()
            return x, y
        

def locateObjectsLeft():
    global x, y, objectLocated, whichObject, switchCounter
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?TRIG')
    time.sleep(2)
    page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?gRES')
    x,y = handleCameraOutput("left", page)
    return x, y

   

def locateObjectsRight():
    global x, y, objectLocated, whichObject, switchCounter
    page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?TRIG')
    time.sleep(2)
    page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?gRES')
    x,y = handleCameraOutput("right", page)
   
        
  
def switchObject():
    global whichObject, switchCounter
    switchCounter += 1
    if whichObject == 0:
        # Looks for Type 1 object
        page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_1')
        time.sleep(3)
    if whichObject == 1:
        # Looks for Type 2 object
        page = urllib.request.urlopen('http://10.1.1.8/CmdChannel?sINT_1_0')
        time.sleep(3)
    time.sleep(1)
    print("object switched")

def checkLeftCamera(): 
#    while switchCounter < 3:
    return locateObjectsLeft()
#        switchObject()

def checkRightCamera(): 
    while switchCounter < 3:
        locateObjectsRight()
        switchObject()


checkLeftCamera()
