#!/usr/bin/env python

import logging

from views.users import UserListHandler, UserProfileHandler, UserVoteHandler
from views.questions import QuestionListHandler, QuestionHandler
from views.importer import ImportQuestionsHandler, ImportMPVotesHandler, ImportUsersHandler

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

def main():

    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([

    	('/users/(.*)/question/(.*)', UserVoteHandler),
    	('/users/(.*)', UserProfileHandler),
    	('/users', UserListHandler),

        ('/questions', QuestionListHandler),
        ('/questions/(.*)', QuestionHandler),
        ('/import/questions', ImportQuestionsHandler),
        ('/import/mpvotes', ImportMPVotesHandler),
        ('/import/users', ImportUsersHandler),

    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()