import logging

from google.appengine.ext import db

class User(db.Expando):
	first_name = db.StringProperty()
	last_name = db.StringProperty()
	postcode = db.StringProperty()
	constituency = db.StringProperty()

class Division(db.Expando):
	summary = db.StringProperty()
	date = db.DateTimeProperty()


class Vote(db.Expando):
	selection = db.StringProperty()


class Constituency(db.Expando):
	name = db.StringProperty()
	mp = db.StringProperty()


class MP(db.Expando):

	first_name = db.StringProperty()
	last_name = db.StringProperty()
	constituency = db.StringProperty()