import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db

from models import User, Question, UserVote

class QuestionHandler(webapp.RequestHandler):

	def get(self, question_key):

		response = {
			"status": 200,
		}

		try:
			question = Question.get(question_key)
			q = db.to_dict(question)
			q['date'] = str(question.date)
			response['question'] = q
		except:
			response['status'] = 404
			response['error'] = 'Cannot find question'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))


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


class QuestionListHandler(webapp.RequestHandler):
	def get(self):
		response = {
			'status': 200,
			'questions': []
		}

		for question in Question.all():
			q = db.to_dict(question)
			q['date'] = str(question.date)
			q['details'] = '/questions/%s' % str(question.key())

			response['questions'].append(q)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))
