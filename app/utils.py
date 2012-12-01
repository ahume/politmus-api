import json
import logging
import datetime
from dateutil.relativedelta import relativedelta

from google.appengine.ext import db

from models import UserVote, MPVote, Question

score_matching = {
	'aye': { 'aye': 100 },
	'no': { 'no': 100 },
	'both': { 'aye': 20, 'no': 20, 'dont-care': 50 }
}

def calculate_score(m, u):
	try:
		return score_matching[m][u]
	except:
		return 0

def compareMP(user):
	# Calculating MP match in real time. Should do this once, when votes are inserted.
	questions = Question.all()

	# Get UserVotes and capture the IDs
	user_votes = UserVote.all().filter('user_username =', user.username)
	question_ids = [a.question for a in user_votes]

	both_voted_on = 0
	exact_match_on = 0
	score = 0

	# Get MPVotes for the appropriate UserVotes

	for u_vote in user_votes:
		mp_vote = MPVote.all().filter('question =', u_vote.question)
		if mp_vote.count() > 0:
			both_voted_on = both_voted_on + 1
			if score == 100:
				exact_match_on = exact_match_on + 1
			score = score + calculate_score(mp_vote[0].selection, u_vote.selection)

	if user_votes.count() > 0:
		score = score / user_votes.count()

	return {
		'both_voted_on': both_voted_on,
		'exact_match_on': exact_match_on,
		'politmus_score': score
	}


def getAnsweredQuestionsFor(username):
	return UserVote.all().filter('username =', username)


def getUnansweredQuestionsFor(username):
	vote_ids = [a.question for a in getAnsweredQuestionsFor(username)]

	question_ids = [str(q.key()) for q in Question.all()]
	filtered_ids = []
	for qid in question_ids:
		if qid not in vote_ids:
			filtered_ids.append(qid)
	questions = Question.get(filtered_ids)
	return questions

def question_to_dict(question):
	q = db.to_dict(question)
	q['date'] = str(question.date)	
	q['key'] = str(question.key())
	q['details'] = '/questions/%s' % str(question.key())
	return q

def mp_to_dict(mp):
	m = db.to_dict(mp)
	m['details'] = '/mps/%s' % mp.slug
	return m

def user_to_dict(user):
	u = db.to_dict(user)
	if isinstance(user.birth_date, datetime.date):
		u['birth_date'] = user.birth_date.isoformat()
	u['details'] = '/users/%s' % user.username
	del u['constituency_score']
	del u['mp_score']
	return u

class QueryFilter(object):

	def filterQueryOnParam(self, param):
		q = self.request.get(param)
		if q is not '':
			self.query.filter(param + ' =', q)

	def addPagingFilters(self, response):
		try:
			start_index = int(self.request.get('start_index')) - 1
			response['start_index'] = start_index + 1
		except:
			start_index = 0
		try:
			count = int(self.request.get('count'))
			response['count'] = count
		except:
			count = 10
		
		self.query = self.query[start_index:start_index+count]
		return response

	def addAgeFilter(self):
		min_age = self.request.get('min_age', None)
		max_age = self.request.get('max_age', None)

		now = datetime.date.today()
		if min_age is not None:
			min_date = now - relativedelta(years=int(min_age))
			self.query.filter('birth_date <', min_date)
		if max_age is not None:
			max_date = now - relativedelta(years=int(max_age) + 1)
			self.query.filter('birth_date >', max_date)


		


class JsonAPIResponse(object):

	def returnJSON(self, code, response):
		response['status'] = code
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))
