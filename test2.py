import urllib.request
import time


print("set right cube")
page = urllib.request.urlopen('http://10.1.1.7/CmdChannel?sINT_1_0')
time.sleep(3)