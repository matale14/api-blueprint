import time, webbrowser
import flask
from flask import g
import os, binascii
from flask import make_response, request
import configparser
import platform


config = configparser.ConfigParser()

if platform.system() == "Windows":
	config.read('app\ClientAPI\onlineid.ini')
elif platform.system() =="Darwin":
	config.read('app/ClientAPI/onlineid.ini')
elif platform.system() =="Linux":
	config.read('app/ClientAPI/onlineid.ini')
company_id = config['DEFAULT']['company id']

"""
try: lines = open("app\onlineid.cfg").read().splitlines()
except IndexError:
	print("Please add the company key you received in an email. If you did not receive one, please contact us.")
company_id = lines[1]"""

def create_token():
	token = binascii.b2a_hex(os.urandom(15))
	return token

	
def setcookie(token):
	resp = make_response("Setting Cookie1!")
	resp.set_cookie("ONLID", token)
	return ""

def setcookie2(token1, comp_id):
	resp = make_response("Setting Cookie2!")
	resp.set_cookie("comp_id", comp_id)
	return ""

	
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
	
def conn_to_hq(token, comp_id):
	send = "client_login|{}|{}".format(comp_id, token)
	setcookie(token)
	b = send.encode()
	print(b)
	requested_data = connect(b)
	
def onlineID():
	token = create_token()
	setcookie(token)
	setcookie(company_id)
	webbrowser.open_new("http://localhost:5000/ex_login")