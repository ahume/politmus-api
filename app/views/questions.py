import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db

from models import User, Question, UserVote
import utils

class QuestionHandler(webapp.RequestHandler, utils.JsonAPIResponse):

	def get(self, question_key):

		response = {}

		try:
			question = Question.get(question_key)
			response['question'] = utils.question_to_dict(question)
		except:
			response['error'] = 'Cannot find question'
			self.returnJSON(404, response)

		self.returnJSON(200, response)


"""
	def get(self, question_key):
		try:
			question = Question.get(question_key)
			user = User.all().filter('username =', self.request.get('username'))[0]
		except:
			self.response.out.write('Question or User not valid')
			return

		# Check if user has already voted on this question.
		already_voted = False
		if UserVote.all().filter('username =', user.username).filter('question =', question_key).count() > 0:
			already_voted = True

		context = {
			'question': question,
			'user': user,
			'already_voted': already_voted
		}

		t = template.render('templates/question.html', context)
		self.response.out.write(t)
"""


class QuestionListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):

	def get(self):

		response = {}

		self.query = Question.all()
		response['total'] = self.query.count()
		response = self.addPagingFilters(response)
		response['questions'] = [utils.question_to_dict(q) for q in self.query]

		self.returnJSON(200, response)
