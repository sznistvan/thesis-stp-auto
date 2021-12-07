#!/usr/bin/python

# import the ncclient library
from ncclient import manager
import sys

def connection(ip,port,uname,pwd):
	try:
		conn = manager.connect(host=ip, port=port, username=uname, password=pwd,hostkey_verify=False,look_for_keys=False)
		return conn
	except (ncclient.operations.errors.TimeoutExpiredError,ncclient.transport.errors.SSHError):
		print("Connection timed out or could not be established!")

	
