import time
import urllib.request

whichObject = 0

class Camera:
    countCamera = 0
    def __init__(self, ip, side):
        self.ip = ip
        self.side = side    
        
    def getSide(self):
        return self.side

    def getRes(self):
        ip = self.ip
        res = urllib.request.urlopen('http://'+ip+'/CmdChannel?TRIG')
        time.sleep(1)
        res = urllib.request.urlopen('http://'+ip+'/CmdChannel?gRES')
        time.sleep(1)
        return res

    def processRes(self):
        res = self.getRes()
        x_offset = float(50)
        y_offset = float(350)

        #reads output from camera
        coords = res.read().decode('utf-8')
        #splits output
        x1 = coords.split(",")
        #whichObject = int(x1[1])
        objectLocated = int(x1[2])

        # check if no block
        if len(x1) < 2:
            # No block found
            countCamera += 1

        else:
            # NO. Blocks > 0
            if objectLocated == 1:
                y = x1[4]
                x = x1[3]
                x = (float(x) + x_offset) /1000
                y = (float(y) - y_offset) /1000
                print("x,y: " + str(y))
                time.sleep(3)
                countCamera = 0
                return x, y
            
            # try three times before fail
            if countCamera < 3:
                self.processRes()
            else: 
                print("Unable to process result from camera")
                raise Exception 
                
    
    def checkForBlock(self):
        '''Check for block'''
        camera = self
        x, y = camera.processRes()
        return x, y

    def switchObjectType(self):
        global whichObject
        camera = self
        ip = camera.ip
        
        if whichObject == 0:
            whichObject += 1
            page = urllib.request.urlopen('http://'+ ip +'/CmdChannel?sINT_1_1')
            time.sleep(3)
        
        if whichObject == 1:
            whichObject -= 1
            page = urllib.request.urlopen('http://'+ ip +'/CmdChannel?sINT_1_0')
            time.sleep(3)
            
        
        print("object switched")



if __name__ == "__main__":
    #camera ip adresses
    cameraLeft = Camera("10.1.1.8", "left")
    cameraRight = Camera("10.1.1.7", "right")
    resultCameraLeft = cameraLeft.processRes()
    resultCameraRight = cameraRight.processRes()
