import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


from models import User, UserVote, Question, MPVote
import utils

class UserListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):

	def get(self):
		response = {
			'users': []
		}

		self.query = User.all()
		response['total'] = self.query.count()
		self.filterQueryOnParam('gender')
		response = self.addPagingFilters(response)

		for user in self.query:
			u = utils.user_to_dict(user)

			response['users'].append(u)

		self.returnJSON(200, response)

class UserProfileHandler(webapp.RequestHandler, utils.JsonAPIResponse):
	def get(self, username):

		response = {}

		try:
			user = User.all().filter('username =', username)[0]
			response['user'] = utils.user_to_dict(user)
		except:
			response['error'] = 'Cannot find username'
			self.returnJSON(404, response)
			return

		response['comparisons'] = {
			'mp': utils.compareMP(user),
			'constituency': {
				'politmus_score': user.constituency_score
			}
		}

		self.returnJSON(200, response)


class UserQuestionListHandler(webapp.RequestHandler, utils.JsonAPIResponse):
	def get(self, username):

		user = User.all().filter('username =', username)[0]

		response = {
			'username': username,
			'questions': []
		}
		for question in utils.getUnansweredQuestionsFor(username):
			response['questions'].append({
				'title': question.title,
				'question': question.question,
				'key': str(question.key())
			})

		self.returnJSON(200, response)