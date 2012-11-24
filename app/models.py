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
	constituency_score = db.IntegerProperty()
	mp_score = db.IntegerProperty()

class MP(db.Expando):
	name = db.StringProperty()
	slug = db.StringProperty()
	constituency = db.StringProperty()
	party = db.StringProperty()
	age = db.StringProperty()
	gender = db.StringProperty()

class UserVote(db.Expando):
	question = db.StringProperty()
	selection = db.StringProperty()
	user_username = db.StringProperty()

class MPVote(db.Expando):
	selection = db.StringProperty()
	question = db.StringProperty()
	mp_name = db.StringProperty()
	mp_slug = db.StringProperty()
	mp_party = db.StringProperty()
	mp_constituency = db.StringProperty()
	mp_whilst = db.BooleanProperty()

class Constituency(db.Expando):
	name = db.StringProperty()
	slug = db.StringProperty()
	mp_name = db.StringProperty()
	mp_party = db.StringProperty()