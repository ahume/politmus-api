#!/usr/bin/env python

import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from views.general import HomePageRedirect
from views.users import UserListHandler, UserProfileHandler, UserQuestionListHandler
from views.mps import MPProfileHandler, MPListHandler
from views.constituencies import ConstituencyHandler, ConstituencyListHandler
from views.questions import QuestionHandler, QuestionListHandler, UserQuestionsListHandler, UserAnsweredQuestionsListHandler, UserUnansweredQuestionsListHandler
from views.uservotes import UserVoteListHandler, UserVoteHandler
from views.mpvotes import MPVoteListHandler
from views.importer import ImportMPVotesHandler, ImportUsersHandler

def main():

    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([

        ('/users/(.*)/answered-questions', UserAnsweredQuestionsListHandler),
        ('/users/(.*)/unanswered-questions', UserUnansweredQuestionsListHandler),
        ('/users/(.*)/questions', UserQuestionsListHandler),
        ('/users/(.*)/votes/(.*)', UserVoteHandler),
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

        ('/', HomePageRedirect),


    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()