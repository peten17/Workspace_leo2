# Workspace_leo2

Group 22 - Portfolio 2

This solution consists of two python-scripts:
1. setup_adhoc.py
2. tcpServer.py

The setup_adhoc-script sets up an ad hoc network called pibot on ip-address 192.168.99.23 and on frequency 2442 MHz.
The script can be run regardless of the PC being on WiFi or not, and regardless of the name of the interface of the networkcard (#phy0 or #phy1). 
Some of the most important commands used in the script are:
  1. os - This executes commands in bash.
  2. subprocess - This executes the command in bash, and returns the output.
See the script for further documentation.

The tcpServer.py script sets up a TCP-server on ip-address 192.168.99.22, port 8080, and listens for commands. 
On boot, our Pi-zero creates an ad-hoc network, called pibot on ip-address 192.168.99.22 and frequency 2442 MHz. This can be seen as the top four commands in the /etc/rc.local-file.
Some of the most important commands used in the script are:
  1. socket - used for creating a TCP-server and recieving messages.
  2. threading - used for running the start-function on another thread. This allows the server to keep listening to messages, and perform these while the robot is running.
This script supports the following commands:
  1. start - starts the robot.
  2. stop - stops the robot.
  3. getdist - returns the distance currently measured by the distance sensor.
  4. getmotors - returns the current motorvalues.
  5. start x - starts the robot and runs it for x iterations.
  
  Made by:
  Peter Nielsen - peten17@student.sdu.dk
  Jens Møller Rossen - jeros17@student.sdu.dk
