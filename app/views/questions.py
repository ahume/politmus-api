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

class UserQuestionsListHandler(webapp.RequestHandler, utils.JsonAPIResponse):

	def get(self, username):

		response = {}

		self.username = username
		self.answered_ids = None

		response['answered_questions'] = [utils.question_to_dict(q) for q in self.getAnsweredQuestions()]
		response['unanswered_questions'] = [utils.question_to_dict(q) for q in self.getUnansweredQuestions()]

		self.returnJSON(200, response)

	def getAnsweredQuestions(self):

		if self.answered_ids is None:
			self.user_votes = UserVote.all().filter('user_username =', self.username)
			self.answered_ids = [v.question for v in self.user_votes]

		return Question.get(self.answered_ids)

	def getUnansweredQuestions(self):

		if self.answered_ids is None:
			self.getAnsweredQuestions()

		question_ids = [str(q.key()) for q in Question.all()]

		filtered_ids = []
		for q in question_ids:
			if q not in self.answered_ids:
				filtered_ids.append(q)

		return Question.get(filtered_ids)



class UserAnsweredQuestionsListHandler(UserQuestionsListHandler, utils.JsonAPIResponse):

	def get(self, username):
		response = {}

		self.username = username
		self.answered_ids = None

		questions = self.getAnsweredQuestions()
		response['total'] = len(questions)
		response['questions'] = [utils.question_to_dict(q) for q in questions]

		self.returnJSON(200, response)

class UserUnansweredQuestionsListHandler(UserQuestionsListHandler, utils.JsonAPIResponse):

	def get(self, username):
		response = {}

		self.username = username
		self.answered_ids = None

		questions = self.getUnansweredQuestions()
		response['total'] = len(questions)
		response['questions'] = [utils.question_to_dict(q) for q in questions]

		self.returnJSON(200, response)


class QuestionListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):

	def get(self):

		response = {}

		self.query = Question.all()
		response['total'] = self.query.count()
		response = self.addPagingFilters(response)
		response['questions'] = [utils.question_to_dict(q) for q in self.query]

		self.returnJSON(200, response)
