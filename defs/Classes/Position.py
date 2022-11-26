class Position:
    # Constructor with all parameters for positions
    def __init__(self, x, y, z, rx, ry, rz):
        self.x = x
        self.y = y    
        self.z = z
        self.rx = rx
        self.ry = ry    
        self.rz = rz
    
    # Constructor with positions only using x and y
#    def __init__(self, x, y):
#        self.x = x
#        self.y = y    
#        self.z = 0
#        self.rx = 0
#        self.ry = 0    
#        self.rz = 0
    
    # To string representation
    def __str__(self):
        return f"{self.x} {self.y} {self.z} {self.rx} {self.ry} {self.rz}"
    
    # Getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def getZ(self):
        return self.z
    
    def getRX(self):
        return self.rx
    
    def getRY(self):
        return self.ry
    
    def getRZ(self):
        return self.rz

    # Setters
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
    
    def setZ(self, z):
        self.z = z
    
    def setRX(self, rx):
        self.rx = rx
    
    def setX(self, ry):
        self.ry = ry
    
    def setX(self, rz):
        self.rz = rz

    # Create via Position to avoid crashes
    def viaPosition(self):
        safeDistance = 0.15
        viaPosZ = self.z + safeDistance
        return Position(self.x, self.y, viaPosZ, self.rx, self.ry, self.rz)