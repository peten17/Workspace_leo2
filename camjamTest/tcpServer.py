from time import sleep
from gpiozero import DistanceSensor, CamJamKitRobot
import socket
import threading

# Global variable
_stop = True
_newRight = 0
_newLeft = 0

# Pin definition
pinTrig = 17
pinEcho = 18 

# IP and port defenition
IP = '192.168.99.22'
PORT = 8080

# General initialization of robot, distancesensor and socket
robot = CamJamKitRobot()
distSens = DistanceSensor(echo=pinEcho, trigger=pinTrig)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((IP,PORT))
sock.listen(1)


# set left and right to a value that makes the robot go straight
FFleft = -0.52
FFright= -0.55 

def getDist():
	return distSens.distance*100

def motorRun(_left, _right):
	left = _left
	right = _right
	motorValue = (left,right)
	robot.value = motorValue

def motorStop():
	print("Motor stopped")
	robot.value = (0,0)

def startTimes(times):
	print("Robot started")

	global _newRight
	global _newLeft

	ref = 20
	gain = 1.3

	for i in range(times):
		error = 0	
		
		# Get data from encoder
		for i in range(1):
			error+= getDist()
		avgError = error/1
		#sleep(0.0001)

		diff = ref - avgError

		
		#	Sets new values for each motor each cycle 
		_newRight = FFright + gain*(FFright*(diff)/100)
		_newLeft = FFleft - gain*(FFleft*(diff)/100)
		#print(str(newLeft) + " " + str(newRight)) 
		motorRun(_newLeft,_newRight)

		#print("Diff: "+ str(diff) + " newLeft/left: " + str(newLeft)+"/"+str(FFleft) + " | newRight/right: " + str(newRight)+ "/" + str(FFright) )
	stop()


def stop():
	print("Robot Stopped")
	global _stop
	_stop = True
	motorStop()
	
def start():
	global _stop
	global _newRight
	global _newLeft
	_stop = False
	
	while _stop == False:
		
		ref = 30
		gain = 1.3
		error = 0	

		# Get data from encoder
		for i in range(1):
			error+= getDist()
		avgError = error/1

		diff = ref - avgError

		#	Sets new values for each motor each cycle 
		_newRight = FFright + gain*(FFright*(diff)/100)
		_newLeft = FFleft - gain*(FFleft*(diff)/100)
		#print(str(newLeft) + " " + str(newRight)) 
		motorRun(_newLeft,_newRight)
		#print("Diff: "+ str(diff) + " newLeft/left: " + str(newLeft)+"/"+str(FFleft) + " | newRight/right: " + str(newRight)+ "/" + str(FFright) )

	stop()
	
def decodeMessage(data):
	# Decodes the data and removes newlines
	decodedData = data.decode().rstrip("\n").split(" ")
	print("Recieved data: " + decodedData[0])
	return decodedData 

def startServer():

	while True:
		conn, addr = sock.accept()
		data = conn.recv(1024)

		message = decodeMessage(data)

		response = commands(message)
		conn.send(str.encode(response))

def commands(command):
	# Checks the message from the client and calls the appropriate function
	if command[0] == "start":
		response = "Robot started\n"				
		if len(command) == 1:
			start_thread = threading.Thread(target=start)
			start_thread.start()
			return response
		else:
			startTimes(int(command[1]))
			return response
	elif command[0] == "stop":
		global _stop
		_stop = True
		response = "Robot stopped\n"
		return response
	elif command[0] == "run":	
		motorRun(float(message[1]),float(message[2]))
		print("data: " + message[1] + " " + message[2])
		response = "Robot running\n"
		return response
	elif command[0] == "getdist":
		response = str(getDist()) + "\n"
		return response
	elif command[0] == "getmotors":
		response = "Left: " + str(_newLeft) + " Right: " + str(_newRight) + "\n"
		return response
	else:
		response = "Not a valid command\n"
		return response	

# -- main -- #
startServer()
