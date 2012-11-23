import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


from models import User, MP, UserVote, Question, MPVote
import utils


class MPListHandler(webapp.RequestHandler):
	def get(self):
		response = {
			'status': 200,
			'mps': []
		}

		for mp in MP.all():
			u = db.to_dict(mp)
			u['details'] = '/mps/%s' % mp.slug

			response['mps'].append(u)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

class MPProfileHandler(webapp.RequestHandler):
	def get(self, slug):

		response = {
			"status": 200,
		}

		try:
			response['user'] = db.to_dict(MP.all().filter('slug =', slug)[0])
		except:
			response['status'] = 404
			response['error'] = 'Cannot find mp'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

class MPVoteHandler(webapp.RequestHandler):
	def get(self, slug, question_key):

		response = {}

		try:
			q = Question.get(question_key)
			response['question'] = db.to_dict(q)
			response['question']['date'] = str(q.date)
			response['selection'] = MPVote.all().filter('mp_slug =', slug).filter('question =', question_key)[0].selection
		except:
			if response['question'] is not None:
				del response['question']
			response['status'] = 404
			response['error'] = 'Cannot find question or mpvote'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

