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
		self.filterQueryOnParam('gender')
		response = self.addPagingFilters(response)

		for user in self.query:
			u = db.to_dict(user)
			u['details'] = '/users/%s' % user.username

			response['users'].append(u)
		response['total'] = len(response['users'])

		self.returnJSON(200, response)

class UserProfileHandler(webapp.RequestHandler, utils.JsonAPIResponse):
	def get(self, username):

		response = {}

		try:
			response['user'] = db.to_dict(User.all().filter('username =', username)[0])
		except:
			response['error'] = 'Cannot find username'
			self.returnJSON(404, response)
			return

		self.returnJSON(200, response)



		"""
		Below here shows how to calculate match scores. Sort of.
		questions = Question.all()

		# Get UserVotes and capture the IDs
		user_votes = UserVote.all().filter('username =', username)
		question_ids = [a.question for a in user_votes]

		match_count = 0
		shared_count = 0
		match_percentage = 0

		# Get MPVotes for the appropriate UserVotes
		if user_votes.count() > 0:
			mp_votes = MPVote.all().filter('name =', user.mp).filter('question IN', question_ids)
			shared_count = mp_votes.count()

			# Count the votes that match.
			for vote in mp_votes:
				if UserVote.all().filter('username =', username).filter('question =', vote.question)[0].selection == vote.selection:
					match_count = match_count + 1


		context = {
			'user': user,
			'questions': questions,
			'shared_count': shared_count,
			'match_count': match_count,
			'match_percentage': match_percentage
		}

		t = template.render('templates/users_user.html', context)
		self.response.out.write(t)
		"""

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