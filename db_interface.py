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

	Ventures = relationship("Venture", primaryjoin = "Venture.CreatorID == Person.PersonID", backref="Creator")

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return PersonID

	def __repr__(self):
		return '<User %r>' % (self.PersonID)

class Venture(Base):
	__tablename__ = 'Ventures'
	Title = Column(String(20), primary_key = True)
	ShortDesc = Column(String(300))
	Backers = Column(Integer)
	CreatorID = Column(Integer, ForeignKey('Persons.PersonID'))
	
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
	
def get_person_by_id(id, password = None):
	session = Session()
	person = session.query(Person).options(joinedload(Person.Campaigns).joinedload(Campaign.IndividualContributions)).filter(Person.PersonID == id)
	
	if(password):
		person = person.filter(Person.Password == password)
	
	person = person.first()
	session.close()
	
	return person