import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


from models import User, MP, Constituency, UserVote, Question, MPVote
import utils


class ConstituencyListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):
	def get(self):
		response = {
			'constituencies': []
		}

		for const in Constituency.all():
			c = db.to_dict(const)
			c['details'] = '/constituencies/%s' % const.slug

			response['constituencies'].append(c)

		self.returnJSON(200, response)

class ConstituencyHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):
	def get(self, slug):

		response = {}

		try:
			response['constituency'] = db.to_dict(Constituency.all().filter('slug =', slug)[0])
		except:
			response['error'] = 'Cannot find constituency'
			self.returnJSON(404, response)

		self.returnJSON(200, response)

