from time import sleep
from gpiozero import DistanceSensor, CamJamKitRobot
 
import socket


# Pin definition
pinTrig = 17
pinEcho = 18 


IP = 'localhost'
PORT = 8000


robot = CamJamKitRobot()
distSens = DistanceSensor(echo=pinEcho, trigger=pinTrig)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# set left and right to a value that makes the robot go straigt
FFleft  = -0.33
FFright =-0.3

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

def start(times):
	print("Robot started")

	#--------P-controller---------#
	ref = 25
	gain = 1.3

	for i in range(times):
		newLeft = 0 
		newRight = 0
		# Get data from 
		error = 0	
		for i in range(10):
			error+= getDist()
		avgError = error/10

		diff = ref - avgError
		#print(((gain*abs(diff)))/100)
		if diff > 0.00001:
			newRight = FFright+(0.5*(gain*abs(diff)))/100
			if newRight > 0.99:
				motorRun(FFleft,0.99)
			else:
				motorRun(FFleft,newRight)
				
		elif diff < -0.00001:
			newLeft = FFleft+(0.5*(gain*abs(diff)))/100
			if newLeft > 0.99:
				motorRun(0.99,FFright)
			else: 
				motorRun(newLeft,FFright)
			
		print("Diff: "+ str(diff) + " left: " + str(newLeft) + " right: " + str(newRight) + " Error: " + str(avgError) + " ") 
	stop()


def stop():
	print("Robot Stopped")
	motorStop()


def startServer():
	

	sock.bind((IP,PORT))
	sock.listen(1)
	


	while True:
		conn, addr = sock.accept()	
		data = conn.recv(1024)
		if not data:
			sock.close()
			break
		

		# Decodes the data and removes newlines
		decodedData = data.decode().rstrip("\n").split(" ")
		print("Recieved data: " + decodedData[0])


		# Checks the message from the client and calls the appropiate function
		if decodedData[0] == "start":
			start(int(decodedData[1]))
			respons = "Robot started\n"
			conn.send(str.encode(respons))
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
			respons = "Not at valid command\n"
			conn.send(str.encode(respons))

				


# -- main -- #
startServer()





