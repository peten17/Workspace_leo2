from time import sleep
from gpiozero import CamJamKitRobot

robot = CamJamKitRobot()

robot.stop()

robot.forward()
sleep(3)

robot.backward()
sleep(3)
