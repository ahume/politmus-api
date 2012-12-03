from google.appengine.ext import webapp
from google.appengine.ext import db

from models import MP, MPVote
import utils



class MPVoteListHandler(webapp.RequestHandler, utils.QueryFilter, utils.JsonAPIResponse):
	def get(self, slug):

		response = {}
		try:
			mp = MP.all().filter('slug =', slug)[0]
			response['mp'] = utils.mp_to_dict(mp)
		except:
			self.returnJSON(404, response)
			return

		self.query = MPVote.all().filter('mp_slug =', slug)
		self.filterQueryOnParam('question')
		self.filterQueryOnParam('selection')

		response['votes'] = []
		for vote in self.query:
			d = db.to_dict(vote)
			d['question'] = utils.question_to_dict(vote.parent())
			del d['mp_party']
			del d['mp_constituency']
			del d['mp_slug']
			del d['mp_name']
			response['votes'].append(d)
		response['total'] = len(response['votes'])

		self.returnJSON(200, response)