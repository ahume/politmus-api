import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


from models import User, MP, Constituency, UserVote, Question, MPVote
import utils


class ConstituencyListHandler(webapp.RequestHandler):
	def get(self):
		response = {
			'status': 200,
			'constituencies': []
		}

		for const in Constituency.all():
			c = db.to_dict(const)
			c['details'] = '/constituencies/%s' % const.slug

			response['constituencies'].append(c)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

class ConstituencyHandler(webapp.RequestHandler):
	def get(self, slug):

		response = {
			"status": 200,
		}

		try:
			response['constituency'] = db.to_dict(Constituency.all().filter('slug =', slug)[0])
		except:
			response['status'] = 404
			response['error'] = 'Cannot find constituency'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

