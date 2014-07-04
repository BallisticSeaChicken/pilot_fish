from flask import Flask, flash, url_for, render_template, redirect, request, g, session
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from db_interface import Campaign, all_campaigns, get_campaign_by_title, Person, get_all_persons, get_person_by_id, get_contribution, get_ventures, commit_to_db
from forms import SignUpForm, LogInForm

app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

app.secret_key = 'For mother Russia'

@lm.user_loader
def load_user(id):
    return get_person_by_id(int(id))

@app.before_request
def before_request():
    g.user = current_user	
	
@app.route("/")
def redirect_home():
    return redirect(url_for('home'))

@app.route("/signup", methods=['GET','POST'])
def sign_up():
	form = SignUpForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			print '<-------Submitting---------------'
			PersonID = form.PersonID.data
			FirstName = form.FirstName.data
			LastName = form.LastName.data
			Password = form.Password.data
			Department = form.Department.data
			Position = form.Position.data
			Office = form.Office.data
			PhoneNumber = form.PhoneNumber.data
			Email = form.Email.data
			
			Skill1 = form.Skill1.data
			Skill2 = form.Skill2.data
			Skill3 = form.Skill3.data
			
			Interest1 = form.Interest1.data
			Interest2 = form.Interest2.data
			
			user = Person(PersonID, FirstName, LastName, Password, Department, Position, Office, PhoneNumber, Email, Skill1, Skill2, Skill3, Interest1, Interest2)
			
			user = commit_to_db(user)
		
			login_user(user)
			session['logged_in'] = True
			flash('Signed in successfully')
			return redirect(url_for('person_info', id = user.get_id()))
	
	return render_template('sign_up.html', 
		title = 'Sign Up',
		form = form)
		
@app.route("/login", methods=['GET','POST'])
def log_in():
	if g.user is not None:
		if g.user.is_authenticated():
			flash('Already logged in')
			return redirect(url_for('person_info', id = g.user.get_id()))
	
	form = LogInForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			registered_user = get_person_by_id(form.PersonID.data, form.Password.data)
			if registered_user is None:
				flash('Username or Password is invalid' , 'error')
				return redirect(url_for('log_in'))
			login_user(registered_user)
			session['logged_in'] = True
			flash('Logged in successfully')
			return redirect(url_for('person_info', id = registered_user.get_id()))
		
	return render_template('log_in.html', 
		title = 'Log In',
		form = form)
		
@app.route('/logout')
def logout():
	logout_user()
	session['logged_in'] = False
	return redirect(url_for('home'))
	
@app.route("/ventures/")
def ventures_list():
	ventures = get_ventures()
	return render_template('all_ventures.html', ventures = ventures)
	
@app.route("/home", methods=["GET", "POST"])
def home():
	return render_template('home.html')
	
@app.route("/campaigns/")
def campaigns_list():
	campaigns_list = all_campaigns()
	return render_template('campaigns_all.html', campaigns = campaigns_list)
	
@app.route("/campaigns/<name>")
def campaign_info(name):
	campaign = get_campaign_by_title(name)
	return render_template('single_campaign.html', campaign = campaign)
	
@app.route("/persons/")
def persons_list():
	persons_list = get_all_persons()
	return render_template('persons_all.html', persons = persons_list)

@app.route("/persons/<int:id>")	
def person_info(id):
	person = get_person_by_id(id)
	contributed_to = get_contribution(contributor = id)
	return render_template('single_person.html', person = person, contributed_to = contributed_to)

if __name__ == "__main__":
    app.run(debug = True)