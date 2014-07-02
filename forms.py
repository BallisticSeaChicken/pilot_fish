from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators
from wtforms.validators import Required, DataRequired

class SignUpForm(Form):
	PersonID = TextField('PersonID', validators = [Required()])
	Password = PasswordField('Password', validators = [Required()])
	FirstName = TextField('First Name', validators = [Required()])
	LastName = TextField('Last Name', validators = [Required()])
	Department = TextField('Department', validators = [Required()])
	Position = TextField('Position', validators = [Required()])
	Office = TextField('Office', validators = [Required()])
	Skill1 = TextField('Skill 1', validators = [Required()])
	Skill2 = TextField('Skill 2', validators = [Required()])
	Skill3 = TextField('Skill 3', validators = [Required()])
	Interest1 = TextField('Interest 1', validators = [Required()])
	Interest2 = TextField('Interest 2', validators = [Required()])
	Email = TextField('Email', validators = [Required()])
	PhoneNumber = TextField('Phone Number', validators = [Required()])
	
class LogInForm(Form):
	PersonID = TextField('PersonID', validators = [Required()])
	Password = PasswordField('Password', validators = [Required()])