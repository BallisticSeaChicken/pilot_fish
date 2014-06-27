from flask import Flask, url_for, render_template, redirect
from flask.ext.login import LoginManager
from db_interface import Campaign, all_campaigns, get_campaign_by_title, Person, get_all_persons, get_person_by_id, get_contribution, get_ventures

app = Flask(__name__)
app.secret_key = 'For Mother Russia'
lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(PersonID):
    return get_person_by_id(int(PersonID))

@app.route("/")
def redirect_home():
    return redirect(url_for('home'))
	
@app.route("/ventures")
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