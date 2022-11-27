import time
import urx
#import defs.Classes.Camera as cam
a = 0.3
v = 0.3

rob = urx.Robot("10.1.1.6")
rob.set_tcp((0, 0, 0.16, 0, 0, 0))
time.sleep(0.2)  #leave some time to robot to process the setup commands



rob.movel((0.01,0.01,0.01,0,3.14,0), relative=False)
