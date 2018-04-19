from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, DataRequired, ValidationError

try: lines = open("app\ClientAPI\onlineid.cfg").read().splitlines()
except IndexError:
	print("Please add the company key you received in an email. If you did not receive one, please contact us.")
company_id = lines[1]

def connect(send_data):
	"""
	Connection function shamelessly stolen from server.
	"""
	sender = socket.socket()
	host = socket.gethostname()
	sender_ssl = ssl.wrap_socket(sender)
	if randint(1,2) == 1 :
		port=22025
	else:
		port=22026

	sender_ssl.connect(("88.88.170.2", port))

	print(sender_ssl.getpeername())

	sender_ssl.send(send_data)
	return(sender_ssl.recv().decode())
	sender_ssl.close()
		
def check_password(form, field):
    password_length = len(field.data)
    if password_length >= 8  and (any(char.isdigit() for char in field.data)) and password_length <=15: 
        return True
    else:
        raise ValidationError('Password must be between 8 and 15 characters and include at least 1 number')

def check_email(form, field):
    if set(field.data).issubset(validchars_email):
        if "@" in field.data: 
            if "." in field.data:
                return True
            else:
                return False
        else:
            raise ValidationError('Please enter a valid email address')
    else:
        return False
		
class LoginForm(FlaskForm):
	email = StringField('email', [Required(), check_email])
	otp = StringField('One time Password(Leave blank if you do not have it activated)')
	password = PasswordField('password', [Required(), check_password])
	submit = SubmitField('Login')
	
def online_id():	
	form = LoginForm()
	if form.validate_on_submit():
		try:
			if form.otp.data == "":
				form.otp.data = " "
			else:
				login_data = "login|{}|{}|{}|{}".format(form.email.data, form.password.data, form.otp.data, company_id)
				b = login_data.encode()
				print(b)
				requested_data = connect(b)
				if(requested_data == "login|False"):
					flash("Incorrect information entered.")
				else:
					print(requested_data)
					datajoin = "".join(map(str, requested_data))
					data_list = datajoin.split("|")
					data = data_list[2:12]
					return data
		except Exception as e:
			print(e)
			return None
	else:
		return None