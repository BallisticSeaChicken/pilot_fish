from sqlalchemy import Column, Integer, String, Date, create_engine, ForeignKey
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
	Email = Column(String(50))
	
	Campaigns = relationship("Campaign", backref="person")

class Campaign(Base):
    __tablename__ = 'Campaigns'
    CampaignTitle = Column(String(50), primary_key = True)
    ShortDesc = Column(String(300))
    DatePosted = Column(Date)
    Contributions = Column(Integer)
    Backers = Column(Integer)
    Creator = Column(String(50), ForeignKey('Persons.PersonID'))

def all_campaigns():
	session = Session()
	campaigns = session.query(Campaign).options(joinedload(Campaign.person)).all()
	session.close()
	
	return campaigns
	
def get_campaign_by_title(name):
	session = Session()
	result = session.query(Campaign).filter(campaign.CampaignTitle==name).first()
	session.close()
	
	return result

def get_all_persons():
	session = Session()
	persons = session.query(Person).all()
	session.close()
	
	return persons
	
def get_person_by_id(id):
	session = Session()
	person = session.query(Person).options(joinedload(Person.Campaigns)).filter(Person.PersonID == id).first()
	session.close()
	
	return person