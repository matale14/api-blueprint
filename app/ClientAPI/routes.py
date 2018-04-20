from app import app
from app.ClientAPI.OnlineIdv2 import onlineID, create_token, config_reader
from flask import Blueprint, render_template, flash, make_response, request, redirect, url_for
import webbrowser, datetime

mod = Blueprint('store', __name__, template_folder='templates')

@mod.route('/')
@mod.route('/index')
def index():
	return render_template('store/index.html')
	
	
@mod.route('/setcookie')
def setcookie():
	resp = make_response(redirect(url_for('.onlineid_setup')))
	print("setting token")
	resp.set_cookie("ONLINE_ID_TOKEN", create_token(), max_age=200)
	return resp

def getcookie():
	token = request.cookies.get("ONLINE_ID_TOKEN")
	print("getting token")
	return token
	
def getcookie2():
	token = request.cookies.get("ONLINE_ID_COMPANY")
	print("getting company")
	return token

@mod.route('/setcookie2')
def setcookie2():
	resp = make_response(redirect(url_for('.onlineid_setup')))

	print("setting company ID")
	resp.set_cookie("ONLINE_ID_COMPANY", config_reader(), max_age=200)
	return resp
	
@mod.route('/onlineid_setup')
def onlineid_setup():
	if getcookie() == None:
		return redirect(url_for('.setcookie'))
	elif getcookie2() == None:
		return redirect(url_for('.setcookie2'))
	else:
		webbrowser.open_new("http://localhost:5000/ex_login")
	return render_template('store/onlineid.html')
	
@mod.route('/onlineid_request')
def onlineid_request():
	token = getcookie()
	data = onlineID(token)
	flash("OnlineID PAGE")
	flash(data)
	return render_template('store/onlineid.html')