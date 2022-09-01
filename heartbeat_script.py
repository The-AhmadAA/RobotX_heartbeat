"""A basic hearbeat message generation script for Team Mantis,
by Ahmad Abu-Aysha"""

___author___ = "Ahmad Abu-Aysha"
___email___ = "a.abuaysha@uq.net.au"

from datetime import datetime as dt
import time as clock
from dronekit import connect, VehicleMode, Command, mavutil

# change this to suit system configuration
# in terminal use 'python3 -m serial.tools.miniterm' to find device?
CONNECTION_STRING = '/dev/ttyUSB0'
# CHECK TEAM ID IS CORRECT

def heartbeat():
        """ Pulls in data required to generate a heartbeat message and publishes
	message at a frequency of 1Hz
	Message format is
	Heartbeat Example Message: $RXHRB,111221,161229,21.31198,N,157.88972,W,ROBOT,2,1*11

	where

	Message ID $RXHRB Protocol Header
	AEDT Date 111221 ddmmyy Use Australian Eastern Daylight Time (AEDT)
	AEDT Time 161229 hhmmss (24hr time format) Use Australian Eastern Daylight Time (AEDT)
	Latitude 21.31198 Decimal degrees Provides ~1.11m accuracy N/S indicator N N=north, S=South
	Longitude 157.88972 Decimal degrees Provides ~1.04m accuracy E/W indicator W E=east, W=west
	Team ID ROBOT Team ID5-character code assigned by Technical Director
	System Mode 2 Current mode of AMS 1=Remote Operated 2=Autonomous 3=Killed
	UAV Status 1 Current UAV Status 1=Stowed 2=Deployed 3=Faulted
	The ‘Stowed’ state used only when the UAV is secured to the USV.
	The ‘Deployed’ state is used whenever the UAV is not on board the USV.
	Tools
	Checksum 11 Bitwise XOR
	<CR><LF>
	End of message
	"""
	# message_fields = {
	# 	"message_id" : "$RXHRB", # Static message id
	# 	"aedt_date" : "date",#TODO
	# 	"aedt_time" : "time",#TODO
	# 	"lat" : "123456",#TODO fetch from GPS data
	# 	"N_S" : "S", #TODO fetch from GPS data
	# 	"long" : "123456",#TODO fetch from GPS data
	# 	"E_W" : "E",#TODO fetch from GPS data
	# 	"team_id" : "MANTI", # Assigned by Tech Director (CHANGE TO CONSTANT?)
	# 	"sys_mode" : "1",#TODO fetch sys_mode from central computer?
	# 	"uav_state" : "1",#TODO fetch uav_state from central computer?
	# 	"checksum" : "*11\n\r"
	# 	}

    # create an autopilot connection object
try:
    vehicle = connect(CONNECTION_STRING, wait_ready=True, baud=57600)
except:
    print("unable to connect to vehicle")



while True:

    # fetch lat long from vehicle object
    lat = str(vehicle.location.global_frame.lat)
    long = str(vehicle.location.global_frame.lon)
    date = str(dt.now().date())
    time = "".join([str(dt.now().time().hour), 
            str(dt.now().time().minute),
            str(dt.now().time().second)])

    message_fields = {
    "message_id" : "$RXHRB", # Static message id
    "aedt_date" : date,#TODO
    "aedt_time" : time,#TODO
    "lat" : lat,#TODO fetch from GPS data
    "N_S" : "S", #TODO fetch from GPS data
    "long" : long,#TODO fetch from GPS data
    "E_W" : "E",#TODO fetch from GPS data
    "team_id" : "MANTI", # Assigned by Tech Director (CHANGE TO CONSTANT?)
    "sys_mode" : "1",#TODO fetch sys_mode from central computer?
    "uav_state" : "1",#TODO fetch uav_state from central computer?
    "checksum" : "*11\n\r"
    }
    message = []

    

    # Generate the message string
    for i in message_fields:
            message.append(message_fields[i])
    print(','.join(message))
    clock.sleep(1)


def main():
    print("starting heartbeat script")
    heartbeat()
