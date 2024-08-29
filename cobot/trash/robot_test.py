import frrpc
import time

robot = frrpc.RPC('192.168.58.2')
print("robot is connected")
robot.Mode(0)
robot.SetSpeed(100)
robot.ResetAllError()
robot.ProgramLoad('/fruser/WATERING.lua')
robot.ProgramRun()
cnt = 0
while True:
    state = robot.GetProgramState()
    print(state)
    time.sleep(0.5)
    cnt += 1
    if cnt == 90:
        break
