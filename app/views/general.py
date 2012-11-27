from google.appengine.ext import webapp

class HomePageRedirect(webapp.RequestHandler):
	def get(self):
		self.redirect('/docs/index.html')
