import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import models
from data import import_mp_votes, import_users


class ImportMPVotesHandler(webapp.RequestHandler):
	def get(self):
		import_mp_votes()
		self.response.out.write("Done")

class ImportUsersHandler(webapp.RequestHandler):
	def get(self):
		import_users()
		self.response.out.write("Done")

