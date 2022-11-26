import socket

import time

HOST = "10.1.1.6"
PORT = 30002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




x = -0.190
y = 0.039
x = (float(x) + 25) /1000
y = (float(y) - 385) /1000
s.connect((HOST, PORT))
s.send(("set_digital_out(1,False)"+"\n").encode('utf8'))
s.send(("set_tcp([0,0,0.16,0,0,0])"+"\n").encode('utf8'))

s.send(("movej([" + str(x) + ","+ str(y) + ",0.3,0,0,0])"+"\n").encode('utf8'))
