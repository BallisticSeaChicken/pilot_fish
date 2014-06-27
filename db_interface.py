from sqlalchemy import Column, Integer, String, Date, create_engine, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, joinedload

engine=create_engine('mssql+pyodbc://pilotfish:setinstone@pilotfishdb.c5zdfsvfmy5u.us-west-2.rds.amazonaws.com:1433/FishBase', echo=True)
engine.connect()
Base = declarative_base()
Session = sessionmaker(bind = engine)

class Person(Base):
	__tablename__ = 'Persons'
	PersonID = Column(Integer, primary_key = True)
	FirstName = Column(String(50))
	LastName = Column(String(50))
	Password = Column(String(20))
	Department = Column(String(20))
	PhoneNumber = Column(String(20))
	Email = Column(String(50))
	
	Campaigns = relationship("Campaign", primaryjoin= "Campaign.Creator == Person.PersonID",  backref="Person")
	
	ContributedTo = relationship("Contribution", primaryjoin= "Contribution.ContributorID == Person.PersonID", backref="Contributor")

class Campaign(Base):
	__tablename__ = 'Campaigns'
	CampaignTitle = Column(String(50), primary_key = True)
	ShortDesc = Column(String(300))
	DatePosted = Column(Date)
	Creator = Column(Integer, ForeignKey('Persons.PersonID'))
	
	IndividualContributions = relationship("Contribution", primaryjoin= "Contribution.CampaignName == Campaign.CampaignTitle", backref="ContributionTarget")
	
	def getContributionSum(self):
		sum = int()
		for c in self.IndividualContributions:
			sum += c.Contribution
		return sum
	
	def getNumBackers(self):
		return len(self.IndividualContributions)
	
class Contribution(Base):
	__tablename__ = 'Contributions'
	ContributionID = Column(Integer, primary_key = True)
	ContributorID = Column(Integer, ForeignKey('Persons.PersonID'))
	CampaignName = Column(String, ForeignKey('Campaigns.CampaignTitle'))
	Contribution = Column(Integer)
	
	
def get_contribution(id = None, contributor = None, campaign = None):
	session = Session()
	contributions = session.query(Contribution).options(joinedload(Contribution.Contributor), joinedload(Contribution.ContributionTarget))
	
	if(id):
		contributions = contributions.filter(Contribution.ContributionID == id)
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
	result = session.query(Campaign).options(joinedload(Campaign.Person), joinedload(Campaign.IndividualContributions)).filter(Campaign.CampaignTitle==name).first()
	session.close()
	
	return result

def get_all_persons():
	session = Session()
	persons = session.query(Person).all()
	session.close()
	
	return persons
	
def get_person_by_id(id):
	session = Session()
	person = session.query(Person).options(joinedload(Person.Campaigns).joinedload(Campaign.IndividualContributions)).filter(Person.PersonID == id).first()
	session.close()
	
	return person