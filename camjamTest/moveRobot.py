from time import sleep
from gpiozero import CamJamKitRobot
from gpiozero import DistanceSensor


# Define pins
pinTrig = 17
pinEcho = 18


# initialize instances
distSens = DistanceSensor(echo=pinEcho, trigger=pinTrig)
robot = CamJamKitRobot()


# Varables 
wallLower = 15
wallDist = 20
wallUpper = 25


def start():

	while True:
		robot.stop()
		dist = distSens.distance*100
		print(dist)
		#sleep(1)
		
		
		if (dist < wallLower):
			robot.stop()
			robot.left()
			sleep(0.1)
			robot.stop()
			print("right")
			
		elif (dist > wallUpper):
			robot.stop()
			robot.left()
			sleep(0.1)
			robot.stop()
			print("left")
					
			
			
		robot.backward()
		sleep(.1)
	
		




start()


