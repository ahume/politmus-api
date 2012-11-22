import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from models import User, UserVote, Question, MPVote

class UserListHandler(webapp.RequestHandler):
	def get(self):

		context = {
			'users': User.all(),
		}
		t = template.render('templates/users_list.html', context)
		self.response.out.write(t)

class UserProfileHandler(webapp.RequestHandler):
	def get(self, username):

		try:
			user = User.all().filter('username =', username)[0]
		except:
			self.response.out.write("Cannot find user")
			return

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

class UserVoteHandler(webapp.RequestHandler):
	def post(self, username, question_key):

		try:
			user = User.all().filter('username =', username)[0]
			question = Question.get(question_key)
		except:
			self.response.out.write("Cannot find user or question")

		existing = UserVote.all().filter('username =', user.username).filter('question =', question_key)
		if existing.count() > 0:
			vote = existing[0]
		else:
			vote = UserVote()

		vote.question = question_key
		vote.username = user.username
		vote.constituency = user.constituency
		vote.selection = self.request.get('selection')
		vote.put()

		self.response.out.write('Thanks for voting')

