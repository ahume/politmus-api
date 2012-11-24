import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


from models import User, MP, UserVote, Question, MPVote
import utils


class MPListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):
	def get(self):
		response = {
			'mps': []
		}

		self.query = MP.all()
		response['total'] = self.query.count()
		self.filterQueryOnParam('gender')
		self.filterQueryOnParam('party')
		response = self.addPagingFilters(response)

		for mp in self.query:
			u = db.to_dict(mp)
			u['details'] = '/mps/%s' % mp.slug

			response['mps'].append(u)

		self.returnJSON(200, response)

class MPProfileHandler(webapp.RequestHandler, utils.JsonAPIResponse):
	def get(self, slug):

		response = {}

		try:
			response['mp'] = db.to_dict(MP.all().filter('slug =', slug)[0])
			response['mp']['vote_details'] = '/mps/%s/votes' % slug
		except:
			response['error'] = 'Cannot find mp'
			self.returnJSON(404, response)

		self.returnJSON(200, response)