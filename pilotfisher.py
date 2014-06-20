from flask import Flask, url_for, render_template, redirect
from db_interface import Campaign, all_campaigns, get_campaign_by_title, Person, get_all_persons, get_person_by_id

app = Flask(__name__)

@app.route("/")
def redirect_home():
    return redirect(url_for('home'))
	
@app.route("/home")	
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
	return render_template('single_person.html', person = person)
	

if __name__ == "__main__":
    app.run(debug = True)