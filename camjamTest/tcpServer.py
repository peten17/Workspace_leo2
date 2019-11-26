from time import sleep
#from gpiozero import DistanceSensor, CamJamKitRobot
 
import socket


# Pin definition
pinTrig = 17
pinEcho = 18 

#robot = CamJamKitRobot()
#distSens = DistanceSensor(echo=pinEcho, trigger=pinTrig)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# set left and right to a value that makes the robot go straigt
left = 0
right = 0

def getDist():
	return 10
#	return distSens.distance*100

def motorRun(left, right):
	print(str(left) + " " + str(right))
	#	motorValue = (left,right)
	#	robot.value = motorValue

def motorStop():
	print("Motor stopped")
	#robot.value = (0,0)

def start(times):
	print("Robot started")

	#----------P-controller---------#
	ref = 20
	gain = 1

	for i in range(times):

		# Get data from 
		error = 0	
		for i in range(10):
			error+= getDist()
		avgError = error/10

		diff = ref - avgError

		if diff > 0.1:
			newRight = right*(gain*abs(diff))
			motorRun(left,newRight)
		elif diff < -0.1:
			newLeft = left*(gain*abs(diff))
			motorRun(newLeft,right)


def stop():
	print("Robot Stopped")


def startServer():
	
	IP = 'localhost'
	PORT = 8080

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





