from time import sleep
from gpiozero import DistanceSensor, CamJamKitRobot
import socket
#import sys

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
sock.setblocking(0)


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
	stopped = False
	
	while True:
		try:
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
			message = decodeMessage(data)
			if message[0] == "start" or message[0] == "run":
				response = "Invalid command. Please stop the robot first before attempting to start or run it."
				conn.send(str.encode(response))
			#if message[0] == "exit":
				#stop()
				#stopped = True;
				#break 
			else:
				if message[0] == "stop":
					stopped = True
				response = commands(message)
				conn.send(str.encode(response))
		except:
			pass

		if stopped == True:
			break
	
def decodeMessage(data):
	# Decodes the data and removes newlines
	decodedData = data.decode().rstrip("\n").split(" ")
	print("Recieved data: " + decodedData[0])
	return decodedData 

def startServer():

	while True:
		try:
			conn, addr = sock.accept()
			data = conn.recv(1024)
		
			#print(data)
			#sleep(1)

			message = decodeMessage(data)

			#print(message[0])
			
			#if message[0] == "exit":
				#response = "Server is closing...\n"
				#conn.send(str.encode(response))
				#print("Dab")				
				#sys.exit('Goodbye cruel world!')				
				#conn.close()
				#sock.close()
			if message[0] == "start":
				response = "Robot started\n"
				conn.send(str.encode(response))				
				if len(message) == 1:
					start()
				else:
					startTimes(int(message[1]))
			else:
				response = commands(message)
				conn.send(str.encode(response))
		except:
			pass


		#if not data:
			#sock.close()
			#break

def commands(command):
	# Checks the message from the client and calls the appropriate function
	if command[0] == "stop":
		stop()
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
		response = "Left: " + str(left) + " Right: " + str(right) + "\n"
		return response
	else:
		response = "Not a valid command\n"
		return response	

# -- main -- #
startServer()





