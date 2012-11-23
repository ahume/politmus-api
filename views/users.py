import logging
import os
import json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db


from models import User, UserVote, Question, MPVote
import utils

class UserListHandler(webapp.RequestHandler):
	def get(self):
		response = {
			'status': 200,
			'users': []
		}

		for user in User.all():
			u = db.to_dict(user)
			u['details'] = '/users/%s' % user.username

			response['users'].append(u)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

class UserProfileHandler(webapp.RequestHandler):
	def get(self, username):

		response = {
			"status": 200,
		}

		try:
			response['user'] = db.to_dict(User.all().filter('username =', username)[0])
		except:
			response['status'] = 404
			response['error'] = 'Cannot find username'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))



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

class UserQuestionListHandler(webapp.RequestHandler):
	def get(self, username):

		user = User.all().filter('username =', username)[0]

		logging.debug(user)

		response = {
			'status': 200,
			'username': username,
			'questions': []
		}
		for question in utils.getUnansweredQuestionsFor(username):
			response['questions'].append({
				'title': question.title,
				'question': question.question,
				'key': str(question.key())
			})

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

class UserVoteHandler(webapp.RequestHandler):


	def get(self, username):
		response = {}
		try:
			mp = User.all().filter('username =', username)[0]
			response['user'] = db.to_dict(mp)
			response['status'] = 200
		except:
			response['status'] = 404
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(response))

		user_votes = UserVote.all().filter('user_username =', username)

		logging.debug(user_votes.count())

		question_key = self.request.get('question')
		if question_key is not '':
			user_votes.filter('question =', question_key)

		selection = self.request.get('selection')
		if selection is not '':
			user_votes.filter('selection =', selection)

		response['votes'] = [db.to_dict(v) for v in user_votes]
		for v in response['votes']:
			del v['user_username']

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))



	def post(self, username):

		question_key = self.request.get('question')

		response = {
			'user': username,
			'question': question_key
		}

		allowed_selections = ['aye', 'no', 'dont-care', 'dont-understand']

		if self.request.get('selection') not in allowed_selections:
			response['status'] = 'error'
			response['error'] = 'You did not send a selection [aye, no, dont-care, dont-understand]'
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(response))
			return


		try:
			user = User.all().filter('username =', username)[0]
			question = Question.get(question_key)
		except:
			response['status'] = 404
			response['error'] = 'Cannot find user or question'
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(response))
			return

		# Get existing or new question
		existing = UserVote.all().filter('username =', user.username).filter('question =', question_key)
		if existing.count() > 0:
			vote = existing[0]
		else:
			vote = UserVote()

		vote.question = question_key
		vote.user_username = user.username
		vote.constituency = user.constituency
		vote.selection = self.request.get('selection')
		vote.put()

		response['selection'] = vote.selection
		response['status'] = '200'

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))

