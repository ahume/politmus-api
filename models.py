import logging
from google.appengine.ext import db

class Question(db.Expando):
	title = db.TextProperty()
	question = db.TextProperty()
	summary = db.TextProperty()
	date = db.DateTimeProperty()
	publicwhip_url = db.StringProperty()




class User(db.Expando):
	username = db.StringProperty()
	postcode = db.StringProperty()
	age = db.IntegerProperty()
	gender = db.StringProperty()
	ethnicity = db.StringProperty()
	constituency = db.StringProperty()
	mp = db.StringProperty()


class MP(db.Expando):
	name = db.StringProperty()
	constituency = db.StringProperty()
	age = db.StringProperty()
	gender = db.StringProperty()


class UserVote(db.Expando):
	username = db.StringProperty()
	question = db.StringProperty()
	selection = db.StringProperty()

class MPVote(db.Expando):
	name = db.StringProperty()
	question = db.StringProperty()
	party = db.StringProperty()
	constituency = db.StringProperty()
	selection = db.StringProperty()
	whilst = db.BooleanProperty()




class Constituency(db.Expando):
	name = db.StringProperty()
	mp = db.StringProperty()