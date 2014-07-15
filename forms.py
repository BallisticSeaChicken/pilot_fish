from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, validators, SelectField
from wtforms.validators import Required, DataRequired
from wtforms.widgets import TextArea

class SignUpForm(Form):
	PersonID = TextField('PersonID', validators = [Required()])
	Password = PasswordField('Password', validators = [Required()])
	FirstName = TextField('First Name', validators = [Required()])
	LastName = TextField('Last Name', validators = [Required()])
	Department = TextField('Department', validators = [Required()])
	Position = TextField('Position', validators = [Required()])
	Office = TextField('Office', validators = [Required()])
	
	#choosing skills
	skillSet = [('Arts and Crafts','Arts and Crafts'), ('Outdoors and Athletics', 'Outdoors and Athletics'), ('Science', 'Science'), ('Technology', 'Technology'), ('Communications', 'Communications')]
	Skill1 = SelectField('Skill 1', choices = skillSet, validators = [Required()])
	Skill2 = SelectField('Skill 2', choices = skillSet, validators = [Required()])
	Skill3 = SelectField('Skill 3', choices = skillSet, validators = [Required()])
	
	Interest1 = TextField('Interest 1', validators = [Required()])
	Interest2 = TextField('Interest 2', validators = [Required()])
	Email = TextField('Email', validators = [Required()])
	PhoneNumber = TextField('Phone Number', validators = [Required()])
	
class LogInForm(Form):
	PersonID = TextField('PersonID', validators = [Required()])
	Password = PasswordField('Password', validators = [Required()])

class PostForm(Form):
	body = TextField(u'Text', widget=TextArea(), validators = [Required()])
	