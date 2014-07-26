from flask.ext.wtf import Form, widgets
from wtforms import TextField, BooleanField, PasswordField, validators, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import Required, DataRequired, InputRequired, EqualTo
from wtforms.widgets import TextArea, ListWidget, CheckboxInput

class MultipleCheckboxField(SelectMultipleField):
	widget = ListWidget(prefix_label=False)
	option_widget = CheckboxInput()

class SignUpForm(Form):
	PersonID = TextField('Username', validators = [Required()])
	FirstName = TextField('First Name', validators = [Required()])
	LastName = TextField('Last Name', validators = [Required()])
	Password = PasswordField('Password', [InputRequired(), EqualTo('Confirm', message='Passwords must match')])
	Confirm  = PasswordField('Repeat Password')
	Department = TextField('Department', validators = [Required()])
	Position = TextField('Position', validators = [Required()])
	Office = TextField('Office', validators = [Required()])

	#choosing skills
	skillSet = [('Arts and Crafts','Arts and Crafts'), ('Outdoors and Athletics', 'Outdoors and Athletics'), ('Science', 'Science'), ('Technology', 'Technology'), ('Communications', 'Communications')]
	# create a list of value/description tuples
	Skills = MultipleCheckboxField('Label', choices=skillSet)

	Interest1 = TextField('Interest 1', validators = [Required()])
	Interest2 = TextField('Interest 2', validators = [Required()])
	Email = TextField('Email', validators = [Required()])
	PhoneNumber = TextField('Phone Number', validators = [Required()])
	
class LogInForm(Form):
	PersonID = TextField('Username', validators = [Required()])
	Password = PasswordField('Password', validators = [Required()])

class PostForm(Form):
	body = TextField(u'Text', widget=TextArea(), validators = [Required()])

class DiscussionForm(Form):
	Topic = TextField('Discussion Topic', validators = [Required()])
	Description = TextField(u'Description', widget=TextArea(), validators = [Required()])
	