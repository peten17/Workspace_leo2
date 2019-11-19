
# Script for measuring distance to an object

from time import sleep
from gpiozero import DistanceSensor

# Define pins

pinTrig = 17
pinEcho = 18

sensor = DistanceSensor(echo=pinEcho, trigger=pinTrig)

print("Distance")

while True:
	print("Distance:{}".format(sensor.distance*100))
	sleep(1)
print("----")

