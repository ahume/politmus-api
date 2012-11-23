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
			response['mp'] = db.to_dict(MP.all().filter('slug =', slug)[0])
			response['mp']['vote_details'] = '/mps/%s/votes' % slug
		except:
			response['status'] = 404
			response['error'] = 'Cannot find mp'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))


class MPVoteHandler(webapp.RequestHandler):
	def get(self, slug):

		response = {}
		try:
			mp = MP.all().filter('slug =', slug)[0]
			response['mp'] = db.to_dict(mp)
			response['status'] = 200
		except:
			response['status'] = 404
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(response))

		mp_votes = MPVote.all().filter('mp_slug =', slug)

		logging.debug(mp_votes.count())

		question_key = self.request.get('question')
		if question_key is not '':
			mp_votes.filter('question =', question_key)

		selection = self.request.get('selection')
		if selection is not '':
			mp_votes.filter('selection =', selection)

		response['votes'] = [db.to_dict(v) for v in mp_votes]
		for v in response['votes']:
			del v['mp_party']
			del v['mp_constituency']
			del v['mp_slug']
			del v['mp_name']

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

