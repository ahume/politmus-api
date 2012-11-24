import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


from models import User, MP, UserVote, Question, MPVote
import utils

class MPVoteListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):
	def get(self, slug):

		response = {}
		try:
			mp = MP.all().filter('slug =', slug)[0]
			response['mp'] = utils.mp_to_dict(mp)
		except:
			self.returnJSON(404, response)
			return

		self.query = MPVote.all().filter('mp_slug =', slug)
		self.filterQueryOnParam('question')
		self.filterQueryOnParam('selection')

		response['votes'] = []
		for vote in self.query:
			d = db.to_dict(vote)
			d['question'] = utils.question_to_dict(vote.parent())
			del d['mp_party']
			del d['mp_constituency']
			del d['mp_slug']
			del d['mp_name']
			response['votes'].append(d)
		response['total'] = len(response['votes'])

		self.returnJSON(200, response)



class UserVoteListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):
	def get(self, username):
		response = {}
		try:
			user = User.all().filter('username =', username)[0]
			response['user'] = utils.user_to_dict(user)
		except:
			self.returnJSON(404, response)
			return

		self.query = UserVote.all().filter('user_username =', username)
		self.filterQueryOnParam('question')
		self.filterQueryOnParam('selection')

		response['votes'] = []
		for vote in self.query:
			d = db.to_dict(vote)
			d['question'] = utils.question_to_dict(vote.parent())
			del d['user_username']
			del d['constituency']
			response['votes'].append(d)
		response['total'] = len(response['votes'])

		self.returnJSON(200, response)

	def post(self, username):
		response = self.update(username)
		if response is not None:
			self.returnJSON(201, response)


	def put(self, username):
		response = self.update(username)
		if response is not None:
			self.returnJSON(200, response)



	def update(self, username):

		question_key = self.request.get('question')

		response = {}

		allowed_selections = ['aye', 'no', 'dont-care', 'dont-understand']

		if self.request.get('selection') not in allowed_selections:
			logging.debug("hello")
			response['status'] = 'error'
			response['error'] = 'You did not send a selection [aye, no, dont-care, dont-understand]'
			self.returnJSON(406, response) # 406 Not Acceptable
			return None


		try:
			user = User.all().filter('username =', username)[0]
			question = Question.get(question_key)
		except:
			response['error'] = 'Cannot find user or question'
			self.returnJSON(404, response)
			return None

		# Get existing or new question
		existing = UserVote.all().filter('user_username =', user.username).filter('question =', question_key)
		if existing.count() > 0:
			vote = existing[0]
		else:
			logging.debug(question)
			vote = UserVote(parent=question)

		vote.question = question_key
		vote.user_username = user.username
		vote.constituency = user.constituency
		vote.selection = self.request.get('selection')
		vote.put()

		response['vote'] = db.to_dict(vote)
		del response['vote']['user_username']
		del response['vote']['constituency']


		response['user'] = db.to_dict(user)
		return response

