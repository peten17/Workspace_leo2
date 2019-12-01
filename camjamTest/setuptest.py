import os
import re
import subprocess
from time import sleep

print("Setting up an Ad-hoc network. Please wait 5-10 seconds...")

# Checks if the wifi is turned on. If it is, it is turned off.
# The subprocess.check_output-command executes the command passed in the "" in bash, and returns the output (shell=True).
# The 'nmcli radio wifi'-command returns enabled if the wifi is enabled, and disabled if it is not.
wifistatus = subprocess.check_output("nmcli radio wifi", shell=True)
# The variable 'wifistatus' is parsed to a string.
wifistatus = str(wifistatus)
# The third character of the variable 'wifistatus' is used, because of the special format of the return-value of the subprocess-command. (print the 'wifistatus' variable to see this formatting)
if wifistatus[2] == "e":
	# The os.system-command exectues the command given in the "" in bash. This specific command turns off the wifi.
	os.system("sudo nmcli radio wifi off")
	sleep(5)

# See the above comments for an explanation of the subprocess-command.
# The command 'sudo iw dev | head -n 1' returns the first line of the 'iw dev'-command, which is the name of the interface.
# This can be either #phy0 or #phy1, and is randomly selected when the PC is booted.
output = subprocess.check_output("sudo iw dev | head -n 1", shell=True)
# The variable 'output' is parsed to a string.
output = str(output)
# Here all numbers are extracted from the variable 'output' and saved to the same variable.
output = re.sub('[^0-9]', '', output)

# These commands set up the ad-hoc network. Consult the guides in the project description on Google Drive for further explanation.
# The '{}' in the first command is substituted for the contents of the string 'output', before the command is executed in bash.
# This is done because the name of the interface can be either #phy0 or #phy1, and is initialised randomly on PC-boot.
os.system("sudo iw phy phy{} interface add ibss0 type ibss".format(output))
sleep(1)
os.system("sudo iw ibss0 set type ibss")
sleep(0.5)
os.system("sudo rfkill unblock wifi")
sleep(0.5)
os.system("sudo ip link set ibss0 up")
sleep(0.5)
os.system("sudo iw ibss0 ibss join pibot 2442")
sleep(0.5)
os.system("sudo ip address add 192.168.99.23/16 dev ibss0")

print("Done")
