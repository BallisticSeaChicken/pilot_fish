from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Person(Base):
	__tablename__ = 'Persons'
	PersonID = Column(Integer, primary_key = True, autoincrement=False)
	FirstName = Column(String(50))
	LastName = Column(String(50))
	Password = Column(String(20))
	Department = Column(String(20))
	Position = Column(String(20))
	Office = Column(String(20))
	PhoneNumber = Column(String(20))
	Email = Column(String(50))
	
	Skill1 = Column(String(20))
	Skill2 = Column(String(20))
	Skill3 = Column(String(20))
	
	Interest1 = Column(String(20))
	Interest2 = Column(String(20))
	
	Campaigns = relationship("Campaign", primaryjoin= "Campaign.Creator == Person.PersonID",  backref="Person")
	
	ContributedTo = relationship("Contribution", primaryjoin= "Contribution.ContributorID == Person.PersonID", backref="Contributor")

	Ventures = relationship("Venture", primaryjoin = "Venture.CreatorID == Person.PersonID", backref="Creator")
	
	Comments = relationship('Comment', primaryjoin = 'Comment.Author == Person.PersonID', backref='Commentator')
	
	def get_monthly_contribution(self):
		sum = int()
		today = datetime.datetime.now()
		for c in self.ContributedTo:
			if(c.SubTime.year == today.year and c.SubTime.month == today.month):
				sum += c.Contribution
		return sum
	
	def __init__(self, PersonID, FirstName, LastName, Password, Department, Position, Office, PhoneNumber, Email, Skill1, Skill2, Skill3, Interest1, Interest2):
		self.PersonID = PersonID
		self.FirstName = FirstName
		self.LastName = LastName
		self.Password = Password
		self.Department = Department
		self.Position = Position
		self.Office = Office
		self.PhoneNumber = PhoneNumber
		self.Email = Email
		
		self.Skill1 = Skill1
		self.Skill2 = Skill2
		self.Skill3 = Skill3
		
		self.Interest1 = Interest1
		self.Interest2 = Interest2

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.PersonID

	def __repr__(self):
		return self.FirstName

class Venture(Base):
	__tablename__ = 'Ventures'
	Title = Column(String(50), primary_key = True)
	ShortDesc = Column(String(300))
	Backers = Column(Integer)
	CreatorID = Column(Integer, ForeignKey('Persons.PersonID'))
	
class Campaign(Base):
	__tablename__ = 'Campaigns'
	CampaignTitle = Column(String(50), primary_key = True)
	Description = Column(String(300))
	DatePosted = Column(Date)
	Creator = Column(Integer, ForeignKey('Persons.PersonID'))
	
	IndividualContributions = relationship("Contribution", primaryjoin= "Contribution.CampaignName == Campaign.CampaignTitle", backref="ContributionTarget")
	
	Comments = relationship('Comment', primaryjoin = 'Comment.ParentPost == Campaign.CampaignTitle', backref='TopicCampaign')
	
	def getContributionSum(self):
		sum = int()
		for c in self.IndividualContributions:
			sum += c.Contribution
		return sum
	
	def getNumBackers(self):
		return len(self.IndividualContributions)
	
class Contribution(Base):
	__tablename__ = 'Contributions'
	ContributorID = Column(Integer, ForeignKey('Persons.PersonID'), primary_key = True)
	CampaignName = Column(String(20), ForeignKey('Campaigns.CampaignTitle'), primary_key = True)
	Contribution = Column(Integer)
	SubTime = Column(DateTime, primary_key = True)
	
	def __init__(self, ContributorID, CampaignName, Contribution, SubTime):
		self.ContributorID = ContributorID
		self.CampaignName = CampaignName
		self.Contribution = Contribution
		self.SubTime = SubTime
		
class Comment(Base):
	__tablename__ = 'Comments'
	Key = Column(Integer, primary_key = True)
	ParentPost = Column(String(50), ForeignKey('Campaigns.CampaignTitle'), primary_key = True)
	Author = Column(String(20), ForeignKey('Persons.PersonID'), primary_key = True)
	SubTime = Column(DateTime, primary_key = True)
	Content = Column(Text)
	
	def __init__(self, ParentPost, Author, Content):
		self.ParentPost = ParentPost
		self.Author = Author
		self.SubTime = datetime.datetime.now()
		self.Content = Content