from app import app
from app.ClientAPI.OnlineIdv2 import onlineID, onlineID_set
from flask import Blueprint, render_template, flash, make_response, request, redirect, url_for
import webbrowser, datetime

mod = Blueprint('store', __name__, template_folder='templates')

@mod.route('/')
@mod.route('/index')
def index():
	return render_template('store/index.html')
	
	
@mod.route('/onlineid_setup')
def onlineid_setup():
	onlineID_set()	
	return render_template('store/onlineid.html')
	
@mod.route('/onlineid_request')
def onlineid_request():
	data = onlineID()
	return render_template('store/onlineid.html')
