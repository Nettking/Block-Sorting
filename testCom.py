import urx
import urllib.request
import time


def move(robot, location, moveWait):
    #moves robot
    robot.movex("movep", location,wait=moveWait, acc=0.5, vel=0.8, relative=False, threshold=None)
    if moveWait == False:
        time.sleep(0.1)


r1="10.1.1.5"
#connects to robot
rob = urx.Robot(r1, use_rt=True, urFirm=5.1)

print("[GETTING ROBOT POSE]")
pose = rob.get_pos()
orientation = rob.get_orientation()
print(f"[TCP XYZ][{pose}]")
print(f"[ORIENTATION][{orientation}]")

#positions x, y, z, rx, ry, rz
pos1 = 0.10, -0.22, 0.20, 0, 3.14, 0
pos2 = 0.20, 0.10, 0.20, 0, 3.14, 0
pos3 = 0.03, 0.30, 0.20, 0, 3.14, 0
pos4 = 0.30, 0.30, 0.20, 0, 3.14, 0
pos5 = 0.03, 0.30, 0, 0, 3.14, 0



move(rob, pos1, True)
move(rob, pos2, True)
move(rob, pos3, True)
move(rob, pos4, True)
move(rob, pos5, True)
move(rob, pos3, True)
move(rob, pos2, True)
move(rob, pos1, True)

rob.close()
