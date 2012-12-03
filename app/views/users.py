from uuid import uuid1
import datetime

from google.appengine.ext import webapp

from models import User
import utils

class UserListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):
	def get(self):

		response = {
			'users': []
		}

		self.query = User.all()
		self.filterQueryOnParam('gender')
		self.filterQueryOnParam('ethnicity')
		self.filterQueryOnParam('phone_no')
		self.filterQueryOnParam('postcode')
		self.filterQueryOnParam('constituency')
		self.filterQueryOnParam('mp')
		self.addAgeFilter()
		response['total'] = self.query.count()
		
		response = self.addPagingFilters(response)

		for user in self.query:
			u = utils.user_to_dict(user)

			response['users'].append(u)

		self.returnJSON(200, response)

	def post(self):
		response = {}

		username = self.request.get('username')
		constituency = self.request.get('constituency', None)

		if not constituency:
			response['error'] = 'Must provide a constituency'
			self.returnJSON(402, response)
			return

		user = User()
		user.username = self.request.get('username', uuid1().hex)
		user.first_name = self.request.get('first_name')
		user.last_name = self.request.get('last_name')
		user.street_address = self.request.get('street_address')
		user.locality = self.request.get('locality')
		user.postcode = self.request.get('postcode')
		
		birth_date = self.request.get('birth_date', None)
		if birth_date is not None:
			birth_date = datetime.date(*map(int, birth_date.split("-")))
		user.birth_date	= birth_date

		user.phone_no = self.request.get('phone_no')
		user.email = self.request.get('email')
		user.twitter_username = self.request.get('twitter_username')
		user.gender = self.request.get('gender')
		user.ethnicity = self.request.get('ethnicity')
		user.constituency = self.request.get('constituency')
		user.mp = self.request.get('mp')
		user.constituency_score = 0
		user.mp_score = 0

		user.put()

		response['user'] = utils.user_to_dict(user)
		response['url'] = response['user']['details']

		self.returnJSON(201, response)

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

	def put(self, username):
		response = {}

		try:
			user = User.all().filter('username =', username)[0]
		except:
			response['error'] = 'Cannot find username'
			self.returnJSON(404, response)
			return

		user.first_name = self.request.get('first_name', user.first_name)
		user.last_name = self.request.get('last_name', user.last_name)
		user.street_address = self.request.get('street_address', user.street_address)
		user.locality = self.request.get('locality', user.locality)
		user.postcode = self.request.get('postcode', user.postcode)

		birth_date = self.request.get('birth_date', user.birth_date)
		if isinstance(birth_date, basestring):
			birth_date = datetime.date(*map(int, birth_date.split("-")))
		user.birth_date	= birth_date

		user.phone_no = self.request.get('phone_no', user.phone_no)
		user.email = self.request.get('email', user.email)
		user.twitter_username = self.request.get('twitter_username', user.twitter_username)
		user.gender = self.request.get('gender', user.gender)
		user.ethnicity = self.request.get('ethnicity', user.ethnicity)
		user.constituency = self.request.get('constituency', user.constituency)
		user.mp = self.request.get('mp', user.mp)

		user.put()

		response['user'] = utils.user_to_dict(user)

		self.returnJSON(200, response)

	def delete(self, username):

		response = {}

		try:
			user = User.all().filter('username =', username)[0]
			response['user'] = utils.user_to_dict(user)
			user.delete()
		except:
			response['error'] = 'Cannot find username'
			self.returnJSON(404, response)
			return

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