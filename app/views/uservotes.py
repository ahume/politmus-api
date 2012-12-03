import logging

from google.appengine.ext import webapp

from models import User, UserVote, Question
import utils

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
			response['votes'].append(utils.vote_to_dict(vote))
		response['total'] = len(response['votes'])

		self.returnJSON(200, response)

	def post(self, username):
		question_key = self.request.get('question')
		response = self.update(username, question_key)
		if response is not None:
			self.returnJSON(201, response)

	def update(self, username, question_key):

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

		response['vote'] = utils.vote_to_dict(vote)
		response['user'] = utils.user_to_dict(user)
		return response

class UserVoteHandler(UserVoteListHandler, utils.JsonAPIResponse):
	def get(self, username, question_key):

		response = {}

		try:
			vote = UserVote.all().filter('user_username =', username).filter('question =', question_key)[0]
			response['vote'] = utils.vote_to_dict(vote)
		except:
			response['error'] = 'Cannot find username'
			self.returnJSON(404, response)
			return

		self.returnJSON(200, response)

	def put(self, username, question_key):
		response = self.update(username, question_key)
		if response is not None:
			self.returnJSON(200, response)


	def delete(self, username, question_key):

		response = {}

		try:
			vote = UserVote.all().filter('user_username =', username).filter('question =', question_key)[0]
			vote.delete()
			response['status'] = 200
		except:
			response['error'] = 'Cannot find username'
			self.returnJSON(404, response)
			return

		self.returnJSON(200, response)