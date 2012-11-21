import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import models


class VoteHandler(webapp.RequestHandler):

	def get(self):

		context = {}

		t = template.render('templates/vote.html', context)

		self.response.out.write(t)

