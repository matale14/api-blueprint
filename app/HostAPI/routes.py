import datetime
from datetime import timedelta
import time
from app import app
from app.HostAPI.forms import LoginForm, RegForm, RegisterForm
from flask import render_template, flash, redirect, url_for, session, request, abort, url_for, session, Blueprint
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
import socket, ssl
import pymysql
import bcrypt

mod = Blueprint('host', __name__, template_folder='templates')

@mod.before_request
def before_request():
	"""
	Times user out after minutes of inactivity
	"""
	session.permanent = True
	app.permanent_session_lifetime = datetime.timedelta(minutes=5)
	
@mod.route('/')
@mod.route('/index')
def index():
	"""
	Index set as main route
	"""
	return render_template('index.html', title='Home')
	
	
@mod.route('/delete')	
def delete():
	form = loginForm()
	if form.validate_on_submit():
		try:
			if form.otp.data == "":
				form.otp.data = " "
			else:
				login_data = "deleteuser|{}|{}|{}|".format(form.email.data, form.password.data, form.otp.data)
				b = login_data.encode()
				print(b)
				requested_data = connect(b)
				if(requested_data == "login|False"):
					flash("Incorrect information entered.")
					return render_template('delete.html', title='Delete Account', form=form)
				else:
					flash('Account deleted')
					return redirect(url_for('host.index'))
	return render_template('delete.html', title='Delete Account', form=form)
	
@mod.route('/about')
def about():
	return render_template('about.html', title='About')

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

@mod.route('/register', methods=['GET', 'POST'])
def register():
	"""
	Set form to the wanted one
	send the formatted register info with connect function.
	flashes OTP on the next page.
	"""
	form = RegForm()
	if form.validate_on_submit():
		try:
			data_user = "newuser|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(form.email.data, form.password.data, form.firstname.data, \
			form.lastname.data, form.phone.data, form.zipcode.data, form.country.data, form.countrycode.data, form.address.data, form.addressnumber.data, \
			form.birthday.data, form.sex.data)
			print(data_user)
			b = data_user.encode()
			test_con = connect(b)
			if(test_con == "newuser|false|(False, 'email already in database\n')"):
				flash("Email already in use")
				return redirect(url_for('host.reg_com'))
			else:
				print("successfull: " + test_con)
				setup_otp = "setupotp|{}|{}".format(form.email.data, form.password.data)
				o = setup_otp.encode()
				print(o)
				otp = connect(o)
				datajoin = "".join(map(str, otp))
				data_list = datajoin.split("|")
				data = data_list[3]
				print(data)
				flash(data)
				return redirect(url_for('host.reg_com'))
		except Exception as e:
			print("debug: ", e)
			pass
	print(form.errors)
	return render_template('register.html', title='Register', form=form)
	
	
@mod.route('/reg_com')
def reg_com():
	return render_template('reg_com.html', title='Register')
	
@mod.route('/reg_web', methods=['GET', 'POST'])
def reg_webpage():
	form = RegisterForm()
	if form.validate_on_submit():
		try:
			data_web = "newwebpage|{}|{}|{}|{}|{}|{}|{}".format(form.webname.data, form.email.data, \
			form.contactperson.data, form.phone.data, form.country.data, form.address.data, form.addressnumber.data)
			print(data_web)
			b = data_web.encode()
			flash(connect(b))
			return redirect(url_for('host.index'))
		except TypeError as e:
			print("debug:", e)
			pass
	return render_template('reg_web.html', title='Register', form=form)
		
	
@mod.route('/login', methods=['GET', 'POST'])
def login():
	"""
	Sends request to server
	splits the return into the different information.
	stores the non-sensitive information in session.
	"""
	form = LoginForm()
	if form.validate_on_submit():
		try:
			if form.otp.data == "":
				form.otp.data = " "
			else:
				login_data = "login|{}|{}|{}|KSFPT72MG7C34LNW".format(form.email.data, form.password.data, form.otp.data)
				b = login_data.encode()
				print(b)
				requested_data = connect(b)
				if(requested_data == "login|False"):
					flash("Incorrect information entered.")
					return render_template('login.html', title='Login', form=form)
				else:
					print(requested_data)
					datajoin = "".join(map(str, requested_data))
					data_list = datajoin.split("|")
					data = data_list[2:12]
					#for f in data:
					#	flash(f)
					firstname, lastname, phone, zip, country, countrycode, address, addressnum, birth, sex = data				
					session['logged_in'] = True
					session['firstname'] = firstname
					session['lastname'] = lastname
					session['phone'] = phone
					session['zip'] = zip
					session['country'] = country
					session['countrycode'] = countrycode
					session['address'] = address
					session['addressnum'] = addressnum
					session['birth'] = birth
					session['sex'] = sex
					session['email'] = form.email.data
					return redirect(url_for('host.displayinfo'))
	
		except TypeError as e:
				print("debug:", e)
				pass
	return render_template('login.html', title='Login', form=form)

@mod.route('/displayinfo', methods=['GET', 'POST'])
def displayinfo():
	"""
	redirects user to login if they are not.
	Checks if the data has changed
	sends a request to the server to change information.
	"""
	form = RegForm()
	try:
		if session['logged_in']:
			print("Logged in")
			if form.validate_on_submit():
				changes = []
				if form.firstname.data != session['firstname']:
					s = "firstname|" + form.firstname.data + "|"
					changes.append(s)
				if form.lastname.data != session['lastname']:
					s = "lastname|" + form.lastname.data + "|"
					changes.append(s)
				if form.phone.data != session['phone']:
					s = "phone|" + form.phone.data + "|"
					changes.append(s)
				if form.zipcode.data != session['zip']:
					s = "zipcode|" + form.zipcode.data + "|"
					changes.append(s)
				if form.country.data != session['country']:
					s = "country|" + form.country.data + "|"
					changes.append(s)	
				if form.countrycode.data != session['countrycode']:
					s = "countrycode|" + form.countrycode.data + "|"
					changes.append(s)
				if form.address.data != session['address']:
					s = "address|" + form.address.data + "|"
					changes.append(s)
				if form.addressnumber.data != session['addressnum']:
					s = "addressnumber|" + form.addressnumber.data + "|"
					changes.append(s)
				if form.birthday.data != session['birth']:
					dat = form.birthday.data
					if type(dat) != type(str()):
						t = dat
						birth = t.strftime('%Y-%m-%d')
					else:
						birth = dat
					s = "birthday|" + birth + "|"
					changes.append(s)
				if form.sex.data != session['sex']:
					s = "gender|" + form.sex.data + "|"
					changes.append(s)
				
				try:
					s = "".join(changes)
					edit_data = "edituser|{}|{}|{}".format(session['email'], form.password.data, s)
					print(edit_data)
					b = edit_data()
					connect(b)
					flash("Your information has been changed!")
					return render_template('displayinfo.html', title='Edit Information', form=form)
				except TypeError as e:
					print("debug:", e)
					return redirect(url_for('host.login'))
		else:
			return redirect(url_for('host.login'))
	except KeyError as e:
		print("KeyError:", e)
		return redirect(url_for('host.login'))
		
	return render_template('displayinfo.html', title='Edit Information', form=form)
		

def getcookie1():
	framework = request.cookies.get("ONLID")
	frameworkDem = "supertoken"
	return frameworkDem
	
def getcookie2():
	framework = request.cookies.get("comp_id")
	frameworkDem = "company id"
	return frameworkDem
		
@mod.route("/ex_login")
def ex_login():
	token = getcookie1()
	company_id = getcookie2()
	print(token, company_id)
	form = LoginForm()
	if form.validate_on_submit():
		try:
			if form.otp.data == "":
				form.otp.data = " "
			else:
				login_data = "ex_login|{}|{}|{}|{}".format(form.email.data, form.password.data, form.otp.data, company_id, token)
				b = login_data.encode()
				connect(b)
				return render_template('ex_login_successful.html', title='You can now close this page', form=form)
		except TypeError as e:
				print("debug:", e)
				pass
	return render_template('ex_login.html', title='Login', form=form)
		
@mod.route("/api")
def api():		
	return render_template('api.html', title='API')
		
		
@mod.route('/logout')
def logout():
	session['logged_in'] = False
	session.clear()
	return redirect(url_for('host.index'))
	