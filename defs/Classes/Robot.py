import urx


class Robot:
    def __init__(self, ip, side):
        self.ip = ip
        self.side = side    
        
    def getSide(self):
        return self.side

