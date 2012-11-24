#!/usr/bin/env python

import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from views.users import UserListHandler, UserProfileHandler, UserQuestionListHandler
from views.mps import MPProfileHandler, MPListHandler
from views.constituencies import ConstituencyHandler, ConstituencyListHandler
from views.questions import QuestionHandler, QuestionListHandler
from views.votes import UserVoteListHandler, MPVoteListHandler
from views.importer import ImportQuestionsHandler, ImportMPVotesHandler, ImportUsersHandler, DeleteHandler

def main():

    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([

    	('/users/(.*)/votes/(.*)', UserVoteListHandler),
        ('/users/(.*)/votes', UserVoteListHandler),
    	('/users/(.*)', UserProfileHandler),
    	('/users', UserListHandler),

        ('/mps/(.*)/votes', MPVoteListHandler),
        ('/mps/(.*)', MPProfileHandler),
        ('/mps', MPListHandler),

        ('/constituencies/(.*)', ConstituencyHandler),
        ('/constituencies', ConstituencyListHandler),

        ('/questions/(.*)', QuestionHandler),
        ('/questions', QuestionListHandler),

        # Admin importing tools
        ('/import/mpvotes', ImportMPVotesHandler),
        ('/import/users', ImportUsersHandler),
        ('/import/delete', DeleteHandler),


    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()