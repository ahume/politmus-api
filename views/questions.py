import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from models import User, Question, UserVote

class QuestionHandler(webapp.RequestHandler):

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


class QuestionListHandler(webapp.RequestHandler):

	def get(self):

		try: 
			context = {
				'user': User.get(self.request.get('user')),
				'questions': Queston.all()
			}
		except:
			self.response.out.write('User not valid')
			return


		t = template.render('templates/question_list.html', context)

		self.response.out.write(t)
