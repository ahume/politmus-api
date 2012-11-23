#!/usr/bin/env python

import logging

from views.users import UserListHandler, UserProfileHandler, UserVoteHandler, UserQuestionListHandler
from views.mps import MPProfileHandler, MPListHandler, MPVoteHandler
from views.constituencies import ConstituencyHandler, ConstituencyListHandler
from views.questions import QuestionHandler, QuestionListHandler
from views.importer import ImportQuestionsHandler, ImportMPVotesHandler, ImportUsersHandler

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

def main():

    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([

    	('/users/(.*)/questions/(.*)', UserVoteHandler),
        ('/users/(.*)/questions', QuestionListHandler),
    	('/users/(.*)', UserProfileHandler),
    	('/users', UserListHandler),

        ('/mps/(.*)/votes/(.*)', MPVoteHandler),
        ('/mps/(.*)', MPProfileHandler),
        ('/mps', MPListHandler),

        ('/constituencies/(.*)', ConstituencyHandler),
        ('/constituencies', ConstituencyListHandler),

        ('/questions', QuestionListHandler),
        ('/questions/(.*)', QuestionHandler),

        ('/import/questions', ImportQuestionsHandler),
        ('/import/mpvotes', ImportMPVotesHandler),
        ('/import/users', ImportUsersHandler),


    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()