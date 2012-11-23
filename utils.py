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