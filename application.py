import flask
from flask import flash, url_for, render_template, redirect, request, g, session
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from db_interface import  all_campaigns, get_campaign_by_title, get_all_persons, get_person_by_id, get_contribution, get_ventures, commit_to_db, get_comments, get_challenges, get_discussion_by_topic, get_discussion_entries, get_venture_by_title
from db_model import Campaign, Contribution, Comment, Person, Discussion, Challenge, DiscussionEntry
from forms import SignUpForm, LogInForm, PostForm, DiscussionForm
import datetime

application = flask.Flask(__name__)
application.config.from_object('config')
lm = LoginManager()
lm.init_app(application)
lm.login_view = 'login'

application.secret_key = 'For mother Russia'

@lm.user_loader
def load_user(id):
    return get_person_by_id(id)

@application.before_request
def before_request():
	print request.endpoint
	g.user = current_user
	if not g.user.is_authenticated():
		if request.endpoint!='log_in' and request.endpoint!='static' and request.endpoint!='sign_up':
			return redirect(url_for('log_in'))
	
@application.route("/")
def redirect_home():
    return redirect(url_for('home'))
	
@application.route("/discussions/<topic>", methods=['GET', 'POST'])
@application.route("/discussions/<topic>/<int:page>", methods=["GET", "POST"])
def discuss(topic, page = 1):
	discussion = get_discussion_by_topic(topic)
	comments, previous_exists = get_discussion_entries(topic = topic, page = page)
	postForm = PostForm()
	if request.method == 'POST':
		if request.form['btn'] == 'Comment':
			if postForm.validate_on_submit():
				entry = DiscussionEntry(discussion.Topic, g.user.get_id(), postForm.body.data)
				commit_to_db(entry)
			return redirect(url_for('discuss', topic = topic))
	if request.method=='GET':
		return render_template('single_discussion.html', discussion = discussion, comments = comments, page = page, previous_exists = previous_exists, form = postForm)
	
@application.route("/discussions", methods=['GET', 'POST'])
def discussions_all():
	form = DiscussionForm()
	
	if request.method=='POST':
		if form.validate_on_submit():
			ChallengeName = request.form['ChallengeName']
			Topic = form.Topic.data
			Description = form.Description.data
			
			Creator = g.user.get_id()
			DateCreated = datetime.datetime.now()
			
			discussion = Discussion(ChallengeName, Topic, Creator, DateCreated, Description)
			
			commit_to_db(discussion)
			
			return redirect(url_for('discussions_all'))
		else:
			flash("Could not start your new discussion")
			return redirect(url_for('discussions_all'))
			
	if request.method=='GET':
		return render_template('discussions_all.html', challenges = get_challenges(), form = form)

@application.route("/signup", methods=['GET','POST'])
def sign_up():
	form = SignUpForm()
	if request.method == 'POST':
		if form.validate_on_submit() and 1 <= len(form.Skills.data) <= 3:
			PersonID = form.PersonID.data
			FirstName = form.FirstName.data
			LastName = form.LastName.data
			
			Password = form.Password.data
			Department = form.Department.data
			Position = form.Position.data
			Office = form.Office.data
			PhoneNumber = form.PhoneNumber.data
			Email = form.Email.data
			
			Skills = form.Skills.data
			
			Interest1 = form.Interest1.data
			Interest2 = form.Interest2.data
			
			user = Person(PersonID, FirstName, LastName, Password, Department, Position, Office, PhoneNumber, Email, Skills, Interest1, Interest2)
			user = commit_to_db(user)
			
			registered_user = get_person_by_id(PersonID)
			login_user(registered_user)
			
			flash('Signed in successfully')
			return redirect(url_for('person_info', id = g.user.get_id()))
		else:
			flash('Failed to sign up for Pilot Fish Innovation Platform')
			return redirect(url_for('sign_up'))
	
	return render_template('sign_up.html', 
		title = 'Sign Up',
		form = form)
		
@application.route("/login", methods=['GET','POST'])
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
			flash('Logged in successfully')
			return redirect(url_for('person_info', id = registered_user.get_id()))
		
	return render_template('log_in.html', 
		title = 'Log In',
		form = form)
		
@application.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))
	
@application.route("/ventures/")
def ventures_list():
	ventures = get_ventures()
	return render_template('all_ventures.html', ventures = ventures)
	
	#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
@application.route("/ventures/<name>", methods=["GET", "POST"])
def venture_info(name, page = 1):
	venture = get_venture_by_title(name)
	print "<-----------------------------", type(venture), name
	postForm = PostForm()
	return render_template('single_venture.html', venture=venture)

	
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	
@application.route("/home", methods=["GET", "POST"])
def home():
	return render_template('home.html')
	
@application.route("/campaigns/")
def campaigns_list():
	campaigns_list = all_campaigns()
	return render_template('campaigns_all.html', campaigns = campaigns_list)

@application.route("/campaigns/<name>", methods=["GET", "POST"])
@application.route("/campaigns/<name>/<int:page>", methods=["GET", "POST"])
def campaign_info(name, page = 1):
	campaign = get_campaign_by_title(name)
	print "<-----------------------------", campaign.CampaignTitle, name
	comments, previous_exists = get_comments(campaign = name, page = page)
	postForm = PostForm()
	if request.method == 'POST':
		if request.form['btn'] == 'Contribute':
			if int(request.form['amount']) > 0:
				contribution = Contribution(g.user.get_id(), request.form['campaignTitle'], request.form['amount'], datetime.datetime.now())
				commit_to_db(contribution)
				flash('Contributed %s points to %s!' % (request.form['amount'], name))
			else:
				flash('Please contribute non-zero amount')
			return redirect(url_for('campaign_info', name = name))
		elif request.form['btn'] == 'Comment':
			if postForm.validate_on_submit():
				comment = Comment(campaign.CampaignTitle, g.user.get_id(), postForm.body.data)
				commit_to_db(comment)
			return redirect(url_for('campaign_info', name = name))
	
	if g.user is not None and g.user.is_authenticated():
		return render_template('single_campaign.html', campaign = campaign, comments = comments, page = page, previous_exists = previous_exists, form = postForm, contribute_limit = 100 - g.user.get_monthly_contribution())
	else:
		return render_template('single_campaign.html', campaign = campaign, comments = comments, page = page, previous_exists = previous_exists)
	
@application.route("/persons/")
def persons_list():
	persons_list = get_all_persons()
	return render_template('persons_all.html', persons = persons_list)

@application.route("/persons/<id>")	
def person_info(id):
	person = get_person_by_id(id)
	contributed_to = get_contribution(contributor = id)
	return render_template('single_person.html', person = person, contributed_to = contributed_to)

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
	
#<=====================================Utilities==================================>

def usernameIsAvailable(username):
	Persons = get_all_persons()
	unavailableUsernames = [p.Username for p in Persons]
	
	return not (username in unavailableUsernames)
		