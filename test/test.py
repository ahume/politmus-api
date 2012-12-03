import unittest
import json
import urllib2
from urllib import urlencode

hostname = 'http://localhost:8080'
#hostname = 'http://politmus-api.appspot.com'

class PolitmusAPITest(unittest.TestCase):

	def get_data(self, url):
		return json.load(urllib2.urlopen('%s%s' % (hostname, url) ))

	def post_data(self, url, data):
		url = '%s%s' % (hostname, url)
		return json.load(urllib2.urlopen(url, urlencode(data)))

	def put_data(self, url, data):
		url = '%s%s' % (hostname, url)
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(url, urlencode(data))
		request.get_method = lambda: 'PUT'
		return json.loads(opener.open(request).read())

	def delete_data(self, url):
		url = '%s%s' % (hostname, url)
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(url)
		request.get_method = lambda: 'DELETE'
		return json.loads(opener.open(request).read())

class TestMPProfile(PolitmusAPITest):

	def test_profile(self):

		data = self.get_data('/mps/simonkirby')

		self.assertEqual(data['status'], 200)
		self.assertEqual(data['mp']['name'], 'Simon Kirby')
		self.assertEqual(data['mp']['vote_details'], '/mps/simonkirby/votes')
		self.assertEqual(data['mp']['party'], 'con')
		self.assertEqual(data['mp']['constituency'], 'Brighton, Kemptown')
		self.assertEqual(data['mp']['slug'], 'simonkirby')


class TestMPList(PolitmusAPITest):

	def test_list(self):

		data = self.get_data('/mps')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertTrue(len(data['mps']) > 0)
		self.assertIsNotNone(data['mps'][0]['name'])
		self.assertIsNotNone(data['mps'][0]['details'])
		self.assertIsNotNone(data['mps'][0]['party'])
		self.assertIsNotNone(data['mps'][0]['constituency'])
		self.assertIsNotNone(data['mps'][0]['slug'])

	def test_start_index(self):

		data = self.get_data('/mps?start_index=2')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertEqual(data['start_index'], 2)
		self.assertTrue(len(data['mps']) > 0)

	def test_count(self):

		data = self.get_data('/mps?count=2')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 2)
		self.assertEqual(data['count'], 2)
		self.assertEqual(len(data['mps']), 2)

	def test_party_filter(self):

		data = self.get_data('/mps?party=Green')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		for mp in data['mps']:
			self.assertEqual(mp['party'], 'green')



class TestUserProfile(PolitmusAPITest):

	def test_profile(self):

		data = self.get_data('/users/andyhume')

		self.assertEqual(data['status'], 200)
		self.assertEqual(data['user']['username'], 'andyhume')
		self.assertEqual(data['user']['gender'], 'male')
		self.assertEqual(data['user']['birth_date'], "1980-01-20")
		self.assertEqual(data['user']['postcode'], 'BN2 1NB')
		self.assertEqual(data['user']['constituency'], 'Brighton, Kemptown')
		self.assertEqual(data['user']['ethnicity'], 'white')
		self.assertEqual(data['user']['mp'], 'Simon Kirby')

	def test_create_profile(self):

		data = self.post_data('/users', {'username': 'andyhume2', 'constituency': 'Brighton, Kemptown', 'birth_date': '1980-01-20'})
		self.assertEqual(data['status'], 201)
		self.assertEqual(data['user']['username'], 'andyhume2')
		self.assertEqual(data['user']['birth_date'], '1980-01-20')

		data = self.get_data('/users/andyhume2')	
		self.assertEqual(data['status'], 200)
		self.assertEqual(data['user']['username'], 'andyhume2')
		self.assertEqual(data['user']['birth_date'], '1980-01-20')

		data = self.delete_data('/users/andyhume2')

	def test_create_anon_profile(self):

		data = self.post_data('/users', {'constituency': 'Brighton, Kemptown'})
		self.assertEqual(data['status'], 201)
		self.assertEqual(data['user']['constituency'], 'Brighton, Kemptown')
		new_username = data['user']['username']
		self.assertTrue(len(new_username) > 10) # Did we create a UUID for the new user?

		data = self.get_data('/users/%s' % new_username)
		self.assertEqual(data['status'], 200)
		self.assertEqual(data['user']['username'], new_username)

		data = self.delete_data('/users/%s' % new_username)


	def test_update_profile(self):

		data = self.get_data('/users/andyhume')
		self.assertEqual(data['status'], 200)
		self.assertEqual(data['user']['birth_date'], "1980-01-20")

		data = self.put_data('/users/andyhume', {'birth_date': '1980-1-21'})
		self.assertEqual(data['user']['birth_date'], "1980-01-21")

		data = self.put_data('/users/andyhume', {'birth_date': '1980-1-20'})
		self.assertEqual(data['user']['birth_date'], "1980-01-20")


class TestUserList(PolitmusAPITest):

	def test_list(self):

		data = self.get_data('/users')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertTrue(len(data['users']) > 0)
		self.assertIsNotNone(data['users'][0]['username'])
		self.assertIsNotNone(data['users'][0]['gender'])
		self.assertIsNotNone(data['users'][0]['details'])
		self.assertIsNotNone(data['users'][0]['birth_date'])
		self.assertIsNotNone(data['users'][0]['ethnicity'])
	
	def test_gender_filter(self):

		data = self.get_data('/users?gender=female')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		for user in data['users']:
			self.assertEqual(user['gender'], 'female')

	def test_constituency_filter(self):

		data = self.get_data('/users?constituency=Brighton,%20Kemptown')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		for user in data['users']:
			self.assertEqual(user['constituency'], 'Brighton, Kemptown')

	def test_ethnicity_filter(self):

		data = self.get_data('/users?ethnicity=white')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		for user in data['users']:
			self.assertEqual(user['ethnicity'], 'white')

	def test_postcode_filter(self):

		data = self.get_data('/users?postcode=BN2%201NB')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		for user in data['users']:
			self.assertEqual(user['postcode'], 'BN2 1NB')

	def test_age_filters(self):

		data = self.get_data('/users?min_age=32&max_age=33')
		self.assertEqual(len(data['users']), 2) 
		self.assertEqual(data['users'][0]['username'], 'mike')

		data = self.get_data('/users?min_age=40')
		self.assertEqual(len(data['users']), 2) 
		self.assertEqual(data['users'][0]['username'], 'andybudd')

		data = self.get_data('/users?max_age=25')
		self.assertEqual(len(data['users']), 2) 
		self.assertEqual(data['users'][0]['username'], 'kyle')

	def test_start_index(self):

		data = self.get_data('/users?start_index=2')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertEqual(data['start_index'], 2)
		self.assertTrue(len(data['users']) > 0)

	def test_count(self):

		data = self.get_data('/users?count=2')

		self.assertEqual(data['status'], 200)
		self.assertEqual(data['total'], 18)
		self.assertEqual(data['count'], 2)
		self.assertEqual(len(data['users']), 2)

class TestUserQuestionList(PolitmusAPITest):

	def test_list(self):

		data = self.get_data('/users/andyhume/questions')

		self.assertEqual(data['status'], 200)
		#self.assertTrue(data['total'] > 0)
		self.assertEqual(len(data['answered_questions']), 0)
		self.assertTrue(len(data['unanswered_questions']) > 0)

	def test_answered_list(self):

		data = self.get_data('/users/andyhume/answered-questions')

		self.assertEqual(data['status'], 200)
		self.assertEqual(data['total'], 0)
		self.assertEqual(len(data['questions']), 0)

	def test_unanswered_list(self):

		data = self.get_data('/users/andyhume/unanswered-questions')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertTrue(len(data['questions']) > 0)

class TestUserVoteList(PolitmusAPITest):

	def test_uservote_crud(self):

		data = self.get_data('/users/andyhume/votes')
		self.assertEqual(data['status'], 200)
		self.assertEqual(len(data['votes']), 0)

		data = self.get_data('/users/andyhume/unanswered-questions')
		question_key = data['questions'][0]['key']
		data = self.post_data('/users/andyhume/votes', {'selection': 'aye', 'question': question_key})
		self.assertEqual(data['status'], 201)
		self.assertEqual(data['vote']['selection'], 'aye')

		data = self.get_data('/users/andyhume/votes')
		self.assertEqual(len(data['votes']), 1)

		data = self.put_data('/users/andyhume/votes/%s' % question_key, {'selection': 'no'})
		self.assertEqual(data['status'], 200)
		self.assertEqual(data['vote']['selection'], 'no')

		data = self.delete_data('/users/andyhume/votes/%s' % question_key)
		self.assertEqual(data['status'], 200)

		data = self.get_data('/users/andyhume/votes')
		self.assertEqual(len(data['votes']), 0)


class TestQuestionList(PolitmusAPITest):

	def test_list(self):

		data = self.get_data('/questions')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertTrue(len(data['questions']) > 0)
		self.assertIsNotNone(data['questions'][0]['title'])
		self.assertIsNotNone(data['questions'][0]['question'])
		self.assertIsNotNone(data['questions'][0]['key'])
		self.assertIsNotNone(data['questions'][0]['date'])
		self.assertIsNotNone(data['questions'][0]['details'])

	def test_start_index(self):

		data = self.get_data('/questions?start_index=2')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertEqual(data['start_index'], 2)
		self.assertTrue(len(data['questions']) > 0)


	def test_count(self):

		data = self.get_data('/questions?count=2')

		self.assertEqual(data['status'], 200)
		self.assertEqual(data['total'], 11)
		self.assertEqual(data['count'], 2)
		self.assertEqual(len(data['questions']), 2)

class TestMPMatching(PolitmusAPITest):

	def test_matching_data(self):

		# Whack some test user votes in.
		data = self.get_data('/users/andyhume/votes?question=ahBkZXZ-cG9saXRtdXMtYXBpcg4LEghRdWVzdGlvbhgdDA&selection=no')



if __name__ == '__main__':
    unittest.main()
