from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, DataRequired, ValidationError
import datetime
from random import randint


validchars_email = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-_ @')
validchars_name = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ')
genders = ["Male", "Female", "Other", "male", "female", "other"]
countries = ["norway", "sweden", "denmark", "iceland", "united states", "england", "great britain", \
             "germany",]
countrySelect = [("norway", "Norway"), ("sweden", "Sweden"), ("iceland", "Iceland"), ("united states", "United States"), \
("england", "England"), ("great britain", "Great Britain"), ("germany", "Germany"), ("denmark", "Denmark")]
countrycodes = ["0047", "0046", "0045", "00354", "0111", "0044", "0049"]

"""
Modified filters from server, raises errors on the webpage after submission.
"""
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
    
def check_firstname(form, field):
    if set(field.data).issubset(validchars_name):
        return True
    else:
        raise ValidationError('Enter valid characters for your name, A-Z and a-z')
    
def check_lastname(form, field):
    if set(field.data).issubset(validchars_name):
        return True
    else:
        raise ValidationError('Enter valid characters for your name, A-Z and a-z')
    
def check_phonenumber(form, field):
    phone = field.data
    phone = phone.replace(" ", "")
    phone_length = len(phone)
    if phone_length == 8 and (phone.isdigit()):  
        return True
    else:
        raise ValidationError('Enter a valid phonenumber')
    
def check_address(form, field):
    if set(field.data).issubset(validchars_email):
        return True
    else:
        raise ValidationError('Enter valid characters for your address')
    
def check_addressnumber(form, field):
    if field.data.isdigit():
        return True
    else:
        raise ValidationError('addressnumber should be digits only')
    
def check_postcode(form, field):
    if field.data.isdigit():
        return True
    else:
        raise ValidationError('zipcode should be digits only')

def check_country(form, field):
    field.data = field.data.lower()
    if field.data in countries:
        return True
    else:
        raise ValidationError('please enter a valid country')

def check_countrycode(form, field):
    if field.data in countrycodes: 
        return True
    else:
        raise ValidationError('please enter a valid countrycode')

def check_birthday(form, field):
    dat = field.data
    if type(dat) != type(str()):
        t = dat
        birth = t.strftime('%Y-%m-%d')
    else:
        birth = dat
    try:
        if birth != datetime.datetime.strptime(birth, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError('Please use the YYYY-mm-dd format for dates')
        birthday_datetime = datetime.datetime.strptime(birth, "%Y-%m-%d")
        today = datetime.date.today()
        if 13 <= (today.year - birthday_datetime.year -  ((today.month, today.day) < (birthday_datetime.month, birthday_datetime.day))):
            return True
        else:
            raise ValidationError('You must be 13 years of age to use this service')
    except ValueError as err:
        raise ValidationError(err) 
	
def check_gender(form, field):
    if field.data in genders:
        return True
    else:
        raise ValidationError('Please enter a valid gender')

"""
Different types of forms with their rules.
"""
class RegForm(FlaskForm):
    firstname = StringField('Firstname', [Required(), check_firstname])
    lastname = StringField('Lastname', [Required(), check_lastname])
    address = StringField('Address', [Required(), check_address])
    addressnumber = StringField('Adressnumber', [Required(), check_addressnumber])
    zipcode = StringField('Zipcode', [Required(), check_postcode])
    country = SelectField('Country', [Required(), check_country], choices = countrySelect)
    countrycode = StringField('Countrycode', [Required(), check_countrycode])
    sex = SelectField(u'Gender', [Required(), check_gender], choices = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    email = StringField('Email', [Required(), check_email])
    birthday = DateField('Birthday(Safari or Internet Explorer users, please use YYYY-mm-dd format)', [check_birthday], format='%Y-%m-%d')
    phone = StringField('Phone', [Required(), check_phonenumber])
    password = PasswordField('Password', [Required(), check_password])
    submit = SubmitField('Register')
    edit_b = SubmitField('Save Changes')

	
class RegisterForm(FlaskForm):
    contactperson = StringField('Representative', [Required()])
    webname = StringField('Company Name', [Required()])
    email = StringField('Email', [Required(), check_email])
    country = SelectField('Country', [Required(), check_country], choices = countrySelect)
    address = StringField('Address', [Required(), check_address])
    phone = StringField('Phone', [Required(), check_phonenumber])
    addressnumber = StringField('Adressnumber', [Required(), check_addressnumber])
    submit = SubmitField('Register')
	
	
class LoginForm(FlaskForm):
	email = StringField('Email', [Required(), check_email])
	otp = StringField('One time password (Leave blank if you do not have it activated)')
	password = PasswordField('Password', [Required(), check_password])
	submit = SubmitField('Login')
