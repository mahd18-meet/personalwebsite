
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text





class Links(Base):
	__tablename__="links"
	id = Column(Integer, primary_key=True)
	user = Column(String(120),unique =False)
	original_link = Column(String(350),unique =False)
	shortened_link = Column(String(350),unique =True)


	def __init__(self,user,original_link,shortened_link):
		self.user = user
		self.original_link = original_link
		self.shortened_link =shortened_link


	def __repr__(self):
		return self.user, self.original_link, self.shortened_link

