import unittest
import json
import urllib2

hostname = 'http://localhost:8085'

class PolitmusAPITest(unittest.TestCase):

	def get_data(self, url):
		return json.load(urllib2.urlopen('%s%s' % (hostname, url) ))

	def post_data(self, url):
		return json.load(urllib2.urlpost('%s%s' % (hostname, url) ))

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
		self.assertEqual(data['total'], 8)
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
		self.assertEqual(data['user']['age'], 32)
		self.assertEqual(data['user']['postcode'], 'BN2 1NB')
		self.assertEqual(data['user']['constituency'], 'Brighton, Kemptown')
		self.assertEqual(data['user']['ethnicity'], 'white')
		self.assertEqual(data['user']['mp'], 'Simon Kirby')

class TestUserList(PolitmusAPITest):

	def test_list(self):

		data = self.get_data('/users')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		self.assertTrue(len(data['users']) > 0)
		self.assertIsNotNone(data['users'][0]['username'])
		self.assertIsNotNone(data['users'][0]['gender'])
		self.assertIsNotNone(data['users'][0]['details'])
		self.assertIsNotNone(data['users'][0]['age'] > 0)
		self.assertIsNotNone(data['users'][0]['ethnicity'])
	
	def test_gender_filter(self):

		data = self.get_data('/users?gender=female')

		self.assertEqual(data['status'], 200)
		self.assertTrue(data['total'] > 0)
		for user in data['users']:
			self.assertEqual(user['gender'], 'female')

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
		print data



if __name__ == '__main__':
    unittest.main()