import urx
from defs.Robot_Control.Gripper import *
import time
import urllib

class Camera:
    def __init__(self, ip, side,):
        self.ip = ip
        self.side = side    
        
    def getSide(self):
        return self.side

    def getRes(ip):
        res = urllib.request.urlopen('http://'+ip+'/CmdChannel?TRIG')
        time.sleep(2)
        res = urllib.request.urlopen('http://'+ip+'/CmdChannel?gRES')
        return res

    

#camera ip adresses
cameraLeft = Camera("10.1.1.8", "left")
cameraRight = Camera("10.1.1.7", "right")

