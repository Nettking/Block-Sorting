import urx
from defs.Robot_Control.Gripper import *

class Robot:
    def __init__(self, ip, side):
        self.ip = ip
        self.side = side    
        
    def getSide(self):
        return self.side

#set robot ip adresses
r1="10.1.1.6"
r2="10.1.1.5"

robLeft = urx.Robot(r1, use_rt=True, urFirm=5.1)
robRight = urx.Robot(r2, use_rt=True, urFirm=5.1)