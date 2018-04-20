import time, webbrowser
import flask
from flask import g
import os, binascii
from flask import make_response, request
import configparser
import platform
import datetime
import socket, ssl


def config_reader():
	config = configparser.ConfigParser()

	if platform.system() == "Windows":
		config.read('app\ClientAPI\onlineid.ini')
	elif platform.system() =="Darwin":
		config.read('app/ClientAPI/onlineid.ini')
	elif platform.system() =="Linux":
		config.read('app/ClientAPI/onlineid.ini')
	company_id = config['DEFAULT']['company id']
	return company_id

"""
try: lines = open("app\onlineid.cfg").read().splitlines()
except IndexError:
	print("Please add the company key you received in an email. If you did not receive one, please contact us.")
company_id = lines[1]"""

def create_token():
	token = binascii.b2a_hex(os.urandom(16))
	return token


def setcookie(token):
	resp = make_response("Setting Cookie1!")
	expire_date = datetime.datetime.now()
	expire_date = expire_date + datetime.timedelta(minutes=3)
	resp.set_cookie("ONLINE_ID_TOKEN", token, expires = expire_date)
	return resp


def setcookie2(comp_id):
	resp = make_response("Setting Cookie2!")
	expire_date = datetime.datetime.now()
	expire_date = expire_date + datetime.timedelta(minutes=3)
	resp.set_cookie("ONLINE_ID_COMPANY", comp_id, expires = expire_date)
	return resp

	
def connect(send_data):
	"""
	Connection function shamelessly stolen from server.
	"""
	sender = socket.socket()
	host = socket.gethostname()
	sender_ssl = ssl.wrap_socket(sender)

	sender_ssl.connect(("88.91.35.168", 22025))

	print(sender_ssl.getpeername())

	sender_ssl.send(send_data)
	return(sender_ssl.recv().decode())
	sender_ssl.close()
	
	
def onlineID(token):
	send = "confirm|{}".format(token)
	b = send.encode()
	print(b)
	requested_data = connect(b)
	datajoin = "".join(map(str, requested_data))
	data_list = datajoin.split("|")
	data = data_list[2:12]
	return data
	
	