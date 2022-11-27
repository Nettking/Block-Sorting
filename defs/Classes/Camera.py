import time
import urllib

class Camera:
    def __init__(self, ip, side,):
        self.ip = ip
        self.side = side    
        
    def getSide(self):
        return self.side

    def getRes(self):
        ip = self.ip
        res = urllib.request.urlopen('http://'+ip+'/CmdChannel?TRIG')
        time.sleep(2)
        res = urllib.request.urlopen('http://'+ip+'/CmdChannel?gRES')
        time.sleep(2)
        return res

    def processRes(self, res):
        res = self.getRes()
        x_offset = float(25)
        y_offset = float(-385)

        #reads output from camera
        coords = res.read().decode('utf-8')
        #splits output
        x1 = coords.split(",")
        whichObject = int(x1[1])
        objectLocated = int(x1[2])

        # check if no block
        if len(x1) < 2:
            # No block found
            pass # her bør vi ha noen feilhåndtering
        else:
            # NO. Blocks > 0
            if objectLocated == 1:
                y = x1[4]
                x = x1[3]
                x = (float(x) + x_offset) /1000
                y = (float(y) - y_offset) /1000
                time.sleep(3)
                return x, y
    
    def checkForBlock(self):
        camera = self
        res = camera.getRes(camera.ip)
        x, y = camera.processRes(res)
        return x, y




#camera ip adresses
cameraLeft = Camera("10.1.1.8", "left")
cameraRight = Camera("10.1.1.7", "right")

