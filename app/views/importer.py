from google.appengine.ext import webapp

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

