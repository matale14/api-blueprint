import time, webbrowser
import flask
from flask import g
import os, binascii
from flask import make_response, request, redirect, url_for, session
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

def create_token():
	token = binascii.b2a_hex(os.urandom(16))
	return token
	
	
def connect(send_data):

	sender = socket.socket()
	host = socket.gethostname()
	sender_ssl = ssl.wrap_socket(sender)

	sender_ssl.connect(("88.91.35.168", 22025))

	print(sender_ssl.getpeername())

	sender_ssl.send(send_data)
	return(sender_ssl.recv().decode())
	sender_ssl.close()
	
	
def onlineID():
	token = getcookie()
	send = "confirm|{}".format(token)
	b = send.encode()
	print(b)
	requested_data = connect(b)
	datajoin = "".join(map(str, requested_data))
	data_list = datajoin.split("|")
	data = data_list[2:12]
	return data
	
def onlineID_set():
	token = create_token()
	tok = str(token, 'utf-8')
	company = config_reader() 
	tokens = tok + '|' + company
	session['token'] = tok
	link = 'http://localhost:5000/ex_login?tokens=' + tokens
	webbrowser.open_new(link)			
		