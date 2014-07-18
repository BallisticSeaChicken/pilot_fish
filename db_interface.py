from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload, aliased
from db_model import Campaign, Contribution, Comment, Person, Venture
import datetime

engine=create_engine('mssql://pilotfish:setinstone@pilotfishdb.c5zdfsvfmy5u.us-west-2.rds.amazonaws.com:1433/FishBase', echo=True)
engine.connect()
Session = sessionmaker(bind = engine)

def commit_to_db(target):
	print '<-----committing---------------'
	session = Session()
	session.add(target)
	session.commit()
	
	session.close()
	
def get_ventures(title = None, creatorID = None):
	session = Session()
	ventures = session.query(Venture).options(joinedload(Venture.Creator))
	
	if(title):
		ventures = ventures.filter(Venture.Title == title).first()
	elif(creatorID):
		ventures = ventures.filter(Venture.CreatorID == creatorID).all()
	else:
		ventures = ventures.all()
		
	session.close()
	
	return ventures
	
def get_contribution(contributor = None, campaign = None):
	session = Session()
	contributions = session.query(Contribution).options(joinedload(Contribution.Contributor), joinedload(Contribution.ContributionTarget))
	
	if(contributor):
		contributions = contributions.filter(Contribution.ContributorID == contributor)
	if(campaign):
		contributions = contributions.filter(Contribution.CampaignName == campaign)
		
	contributions = contributions.all()
	
	session.close()
	
	return contributions

def all_campaigns():
	session = Session()
	campaigns = session.query(Campaign).options(joinedload(Campaign.Person), joinedload(Campaign.IndividualContributions)).all()
	session.close()
	
	return campaigns
	
def get_campaign_by_title(name):
	session = Session()
	result = session.query(Campaign).options(joinedload(Campaign.Person), joinedload(Campaign.IndividualContributions)).first()
	session.close()
	
	return result
	
def get_comments(campaign, page):
	session = Session()
	
	stmt = session.query(Comment).filter(Comment.ParentPost == campaign).order_by(Comment.Key.desc()).limit(5 * (page-1)).subquery()
	
	comalias = aliased(Comment, stmt)
	
	last_key = session.query(comalias).order_by(comalias.Key).first()
	
	result = session.query(Comment).filter(Comment.ParentPost == campaign)
	
	if last_key:
		result = result.filter(Comment.Key < last_key.Key)
	
	result = result.options(joinedload(Comment.Commentator)).order_by(Comment.Key.desc()).limit(5).all()
	
	session.close()
	
	return result

def get_all_persons():
	session = Session()
	persons = session.query(Person).all()
	session.close()
	
	return persons
	
def get_person_by_id(id, password = None):
	session = Session()
	person = session.query(Person).options(joinedload(Person.Campaigns).joinedload(Campaign.IndividualContributions), subqueryload(Person.ContributedTo)).filter(Person.PersonID == id)
	
	if(password):
		person = person.filter(Person.Password == password)
	
	person = person.first()
	session.close()
	
	return person