import json

from google.appengine.ext import db

from models import UserVote, Question

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
	return q

def mp_to_dict(mp):
	m = db.to_dict(mp)
	m['details'] = '/mps/%s' % mp.slug
	return m

def user_to_dict(user):
	u = db.to_dict(user)
	u['details'] = '/users/%s' % user.username
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
		


class JsonAPIResponse(object):

	def returnJSON(self, code, response):
		response['status'] = code
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(response))