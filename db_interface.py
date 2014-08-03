from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, joinedload, subqueryload, aliased
from db_model import Campaign, Contribution, Comment, Person, Venture, Challenge, Discussion, DiscussionEntry
import datetime
import sys

sys.path.insert(0, '../config')
from config import db_connection

engine=create_engine(db_connection, echo=True)
engine.connect()
Session = sessionmaker(bind = engine)

def commit_to_db(target):
	print '<-----committing---------------'
	session = Session()
	session.add(target)
	session.commit()
	
	session.close()
	
def delete_from_db(target):
	print '<-----------deleting----------------'
	session = Session()
	session.delete(target)
	session.commit()
	
	session.close()
	
def get_discussion_by_topic(topic):
	session = Session()
	discussion = session.query(Discussion).options(joinedload(Discussion.Creator)).filter(Discussion.Topic==topic).first()
	session.close()
	
	return discussion
	
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
	result = session.query(Campaign).options(joinedload(Campaign.Person), joinedload(Campaign.IndividualContributions)).filter(Campaign.CampaignTitle == name).first()
	session.close()
	
	return result

	
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def get_venture_by_title(name):
	session = Session()
	result = session.query(Venture).options(joinedload(Venture.Creator)).first()
	session.close()
	
	return result
	
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	
def get_comments(campaign, page):
	session = Session()
	page_length = 10
	
	first_key = session.query(Comment).order_by(Comment.Key).filter(Comment.ParentPost == campaign).first()
	
	temp = session.query(Comment).options(joinedload(Comment.Commentator)).filter(Comment.ParentPost == campaign).order_by(Comment.Key.desc()).slice((page -1) * page_length, page * page_length).all()
	
	if temp is not None:
		result = temp
		previous_exist = False if (first_key is None) or (first_key.Key == result[-1].Key) else True
	else:
		result = None
		previous_exist = False
	
	session.close()
	
	return result, previous_exist

def get_discussion_entries(topic, page):
	session = Session()
	page_length = 20
	
	first_key = session.query(DiscussionEntry).order_by(DiscussionEntry.Key).filter(DiscussionEntry.ParentPost == topic).first()
	
	temp = session.query(DiscussionEntry).options(joinedload(DiscussionEntry.Commentator)).filter(DiscussionEntry.ParentPost == topic).order_by(DiscussionEntry.Key.desc()).slice((page-1)*page_length, page * page_length).all()
	if temp:
		result = temp
		print first_key.Key, result[-1].Key, "<-----------------------------"
		previous_exist = False if (first_key is None) or (first_key.Key == result[-1].Key) else True
	else:
		result = None
		previous_exist = False
	
	session.close()
	
	return result, previous_exist
	
def get_all_persons(**kwargs):
	session = Session()
	persons = session.query(Person)
	
	if kwargs:
		persons = persons.filter_by(**kwargs)
	
	persons = persons.all()
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
	
def get_challenges():
	session = Session()
	challenges = session.query(Challenge).options(joinedload(Challenge.Discussions), subqueryload(Challenge.Initiator)).order_by(Challenge.DateMade).all()
	
	session.close()
	
	return challenges