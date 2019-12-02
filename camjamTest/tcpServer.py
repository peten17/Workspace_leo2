from time import sleep
from gpiozero import DistanceSensor, CamJamKitRobot
import os
import socket

# Pin definition
pinTrig = 17
pinEcho = 18 

IP = '192.168.99.22'
PORT = 8080

robot = CamJamKitRobot()
distSens = DistanceSensor(echo=pinEcho, trigger=pinTrig)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP,PORT))
sock.listen(1)


# set left and right to a value that makes the robot go straigt
#FFleft  = -0.3
#FFright =-0.33

FFleft = -0.32
FFright= -0.35

# TO-DO:
# Overload start funktion så den stemmer overens med opgavebeskrivelsen.
# Skriv getmotors-funktionen
 

def getDist():
#	return 10
	return distSens.distance*100

def motorRun(_left, _right):
	#print(str(left) + " " + str(right))
	left = _left
	right = _right
	motorValue = (left,right)
	robot.value = motorValue

def motorStop():
	print("Motor stopped")
	robot.value = (0,0)

def startTimes(times):
	print("Robot started")

	#--------P-controller---------#
	ref = 20
	gain = 1.3

	for i in range(times):
		newLeft = 0 
		newRight = 0
		error = 0	
		
		# Get data from encoder
		for i in range(1):
			error+= getDist()
		avgError = error/1
		#sleep(0.0001)

		diff = ref - avgError

		
		#	Sets new values for each motor each cycle 
		newRight = FFright + gain*(FFright*(diff)/100)
		newLeft = FFleft - gain*(FFleft*(diff)/100)
		#print(str(newLeft) + " " + str(newRight)) 
		motorRun(newLeft,newRight)

		print("Diff: "+ str(diff) + " newLeft/left: " + str(newLeft)+"/"+str(FFleft) + " | newRight/right: " + str(newRight)+ "/" + str(FFright) )
	stop()


def stop():
	print("Robot Stopped")
	motorStop()
	
def start():

	#print("in start()")
	
	while True:

		ref = 30
		gain = 1.3

		newLeft = 0 
		newRight = 0
		error = 0	

		# Get data from encoder
		for i in range(1):
			error+= getDist()
		avgError = error/1
		sleep(0.0001)

		diff = ref - avgError


		#	Sets new values for each motor each cycle 
		newRight = FFright + gain*(FFright*(diff)/100)
		newLeft = FFleft - gain*(FFleft*(diff)/100)
		#print(str(newLeft) + " " + str(newRight)) 
		motorRun(newLeft,newRight)
		print("Diff: "+ str(diff) + " newLeft/left: " + str(newLeft)+"/"+str(FFleft) + " | newRight/right: " + str(newRight)+ "/" + str(FFright) )

		conn, addr = sock.accept()
		data = conn.recv(1024)
		decodedData = data.decode().rstrip("\n")

		if decodedData == "stop":
			break

	stop()
	
	

def startServer():
	

	while True:

		conn, addr = sock.accept()
		data = conn.recv(1024)
		
		if not data:
			sock.close()
			break
		
		# Decodes the data and removes newlines
		decodedData = data.decode().rstrip("\n").split(" ")
		print("Recieved data: " + decodedData[0])

		# Checks the message from the client and calls the appropriate function
		if len(decodedData) > 1 and decodedData[0] == "start":
			startTimes(int(decodedData[1]))
			respons = "Robot started\n"
			conn.send(str.encode(respons))
		elif decodedData[0] == "start":
			respons = "Robot started\n"
			conn.send(str.encode(respons))
			start()
		elif decodedData[0] == "stop":
			stop()
			respons = "Robot stopped\n"
			conn.send(str.encode(respons))
		elif decodedData[0] == "run":
			motorRun(float(decodedData[1]),float(decodedData[2]))
			print("data: " + decodedData[1] + " " + decodedData[2])
		elif decodedData[0] == "getdist":
			respons = str(getDist()) + "\n"
			conn.send(str.encode(respons))
		elif decodedData[0] == "getmotors":
			respons = "Left: " + str(left) + " Right: " + str(right) + "\n"
			conn.send(str.encode(respons))
		elif decodedData[0] == "exit":
			respons = "Server is closing..\n"
			conn.send(str.encode(respons))
			conn.close()
			break
		else:
			respons = "Not a valid command\n"
			conn.send(str.encode(respons))

				


# -- main -- #
#sleep(10)
#print("Ready")
startServer()





