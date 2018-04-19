from app import app
from app.ClientAPI.OnlineIdv2 import onlineID
from flask import Blueprint, render_template, flash
import webbrowser

mod = Blueprint('store', __name__, template_folder='templates')

@mod.route('/')
@mod.route('/index')
def index():
	return render_template('store/index.html')
	
@mod.route('/onlineid')
def online_id_login():
	onlineID()
	
	flash("OnlineID PAGE")
	return render_template('store/onlineid.html')