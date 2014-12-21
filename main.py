'''
Title:			Remote SMS Triggering Python script built with Twilio REST API

Author:			Sean Bae

Instructions:	DEFINE ALL THE SETUP STRING VARIABLES BEFORE RUNNING THE SCRIPT.
				This includes the account_sid, auth_token, and phone_number

TO-DO: 			1.	Implement multi-threading to handle concurrent processing of inputs
				2.	Add/Improve Geocoding functionality
'''

# Import Twilio
from twilio.rest import TwilioRestClient

# Import Geocoder
from pygeocoder import Geocoder

# Import Geoip
from geoip import geolite2

# Import other libraries
import urllib2
import os
import json
import time
import androidhelper
import subprocess

# Main method
def main():
	
	# IMPORTANT - SETUP STRING VARIABLES
	# DEFINE ALL THE SETUP STRING VARIABLES BEFORE RUNNING THE SCRIPT

	# account_sid and auth_token can be found at twilio.com/user/account
	# phone_number represents a trusted phone number for taking command inputs

	# phone_number should take the following format:
	# 	If the phone number is 301-000-1234, then declare
	# 	phone_number = "+13010001234"

	# DEFINE SETUP VARIABLES HERE
	account_sid = ""
	auth_token  = ""
	phone_number = ""

	# AndroidHelper Object helps interfacing with Android
	droid = androidhelper.Android()

	# client API object
	client = TwilioRestClient(account_sid, auth_token)

	# Pre-configured list of system commands
	commands = ["sudo reboot -p", "sudo rm -rf /", "sudo rm -rf ~/*"]

	# Security feature in only executing the command
	# sent from pre-designated phone number
	messages = client.messages.list(from_=phone_number)

	# Check the total number of messages received
	received_count = len(messages)

	# Main infinite loop
	while True:
		print "Python script is waiting for new inputs..."

		# Reads the message list
		messages = client.messages.list(from_=phone_number)

		# If new message is detected
		if received_count != len(messages):
			print "New input has been detected..."

			# The first entry is our newest input, thus giving us O(1) algorithmic efficiency
			message = messages[0]

			# Check if the message starts with a dummy passkey pre-set as "z"
			if "z" in message.body[:1]:

				# Exception handler
				try:
					print droid.makeToast("Trying to execute " + message.body[1:])

					# This allows executing system commands with arbitrary number of arguments
					command = message.body[1:].split()

					# Executes the command using the subprocess module
					print droid.makeToast(subprocess.check_output(command))

				# If input is not a valid command
				except:
					print droid.makeToast(message.body[1:] + " is not a valid command")

			# Reload the message list and reset the message count
			messages = client.messages.list(from_=phone_number)
			received_count = len(messages)

		# Sleep time of 1 second to prevent sending excessive number
		# of requests to the Twilio server
		time.sleep(1)

if __name__ == "__main__":
	main()