from rest_framework import status
from rest_framework.test import APITestCase

from django.core.urlresolvers import reverse

from django.contrib.auth import get_user_model

from survey.models import Question, Answer
User = get_user_model()

class Tests(APITestCase):
	def setUp(self):
		user1 = User(username='testuser', email='test@test.com')
		user1.set_password('password')
		user1.save()
		question = Question.objects.create(question_text='awd',starting_age=1,section=1)
		answer = Answer.objects.create(user=user1,question=question,rating=2)

	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_question(self):
		question_count = Question.objects.count()
		self.assertEqual(question_count, 1)

	def test_single_answer(self):
		answer_count = Answer.objects.count()
		self.assertEqual(answer_count, 1)

	def test_question_list(self):
		data = {}
		url = ''
		printf(url)
'''
		response = self.client.get(url, data, format='json')
		print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print(response.data)
'''