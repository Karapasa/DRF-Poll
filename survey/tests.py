import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Choice, Answer, Survey, Question
from .serializers import *


class SetUp(APITestCase):

    def setUp(self):
        today = timezone.now()
        start_datetime = (today - datetime.timedelta(days=1))
        end_datetime = (today + datetime.timedelta(days=1))
        self.admin = User.objects.create_superuser(username="Test-admin", password="admin", email="admin@host.ru")
        self.user = User.objects.create_user(username="Test-user", password="user", email="user@host.ru")
        self.survey = Survey.objects.create(name='тестовый опрос',
                                            description='тестовое описание',
                                            start_at=start_datetime,
                                            end_at=end_datetime,
                                            is_active=True)
        self.question = Question.objects.create(text='Тестовый вопрос 1',
                                                type_question='text',
                                                survey=self.survey)

        self.question_choice = Question.objects.create(text='Тестовый вопрос 2',
                                                type_question='choice',
                                                survey=self.survey)

        self.choice = Choice.objects.create(question=self.question_choice,
                                            text='test')

        self.answer = Answer.objects.create(user=self.user,
                                            question=self.question,
                                            answer='Тестовый ответ')
        self.anonim_answer = Answer.objects.create(anonymous_id=1,
                                                   question=self.question,
                                                   answer='Тестовый ответ')
        self.user_client = APIClient()
        self.user_client.login(username='Test-user', password='user')
        self.admin_client = APIClient()
        self.admin_client.login(username='Test-admin', password='admin')
        self.anonim_client = APIClient()
        return super().setUp()


class SurveyTest(SetUp, APITestCase):

    def test_get_list(self):
        response = self.user_client.get(reverse('surveys-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_survey(self):
        response = self.user_client.get(reverse('survey-detail', kwargs={'pk': self.survey.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_survey(self):
        today = timezone.now()
        data = {'name': 'тестовый опрос 2',
                'description': 'тестовое описание 2',
                'start_at': today,
                'end_at': today + datetime.timedelta(days=3),
                'is_active': True}
        response_admin = self.admin_client.post(reverse('surveys-list'), data, format='json')
        response_user = self.user_client.post(reverse('surveys-list'), data, format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_post__invalid_date_survey(self):
        today = timezone.now()
        data = {'name': 'тестовый опрос 3',
                'description': 'тестовое описание 3',
                'start_at': today,
                'end_at': today - datetime.timedelta(days=3),
                'is_active': True}
        response_admin = self.admin_client.post(reverse('surveys-list'), data, format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_survey(self):
        data = {'name': 'измененный тестовый опрос',
                'description': 'тестовое описание'}
        response_admin = self.admin_client.put(reverse('survey-detail', kwargs={'pk': self.survey.pk}),
                                               data,
                                               format='json')
        response_user = self.user_client.put(reverse('survey-detail', kwargs={'pk': self.survey.pk}),
                                             data,
                                             format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_invalid_start_at(self):
        data = {'start_at': datetime.datetime.today()}
        response_admin = self.admin_client.put(reverse('survey-detail', kwargs={'pk': self.survey.pk}),
                                               data,
                                               format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_survey(self):
        response_user = self.user_client.delete(reverse('survey-detail', kwargs={'pk': self.survey.pk}),
                                                format='json')
        response_admin = self.admin_client.delete(reverse('survey-detail', kwargs={'pk': self.survey.pk}),
                                                  format='json')
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_admin.status_code, status.HTTP_204_NO_CONTENT)


class QuestionTest(SetUp, APITestCase):

    def test_get_questions_list(self):
        response_admin = self.admin_client.get(reverse('questions-list'), format='json')
        response_user = self.user_client.get(reverse('questions-list'), format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_question_detail(self):
        response = self.admin_client.get(reverse('question-detail', kwargs={'pk': self.question.pk}),
                                         format='json')
        response_user = self.user_client.get(reverse('question-detail', kwargs={'pk': self.question.pk}),
                                             format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_question(self):
        data = {'text': 'тестовый вопрос 3',
                'type_question': 'choice',
                'survey': self.survey.pk}
        response_admin = self.admin_client.post(reverse('questions-list'), data, format='json')
        response_user = self.user_client.post(reverse('questions-list'), data, format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_question(self):
        data = {'text': 'изменненый тестовый опрос 2',
                'type_question': 'text',
                'survey': self.survey.pk}
        response_admin = self.admin_client.put(reverse('question-detail', kwargs={'pk': self.question.pk}),
                                               data,
                                               format='json')
        response_user = self.user_client.put(reverse('question-detail', kwargs={'pk': self.question.pk}),
                                             data,
                                             format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_question(self):
        response_user = self.user_client.delete(reverse('question-detail', kwargs={'pk': self.question.pk}),
                                                format='json')
        response_admin = self.admin_client.delete(reverse('question-detail', kwargs={'pk': self.question.pk}),
                                                  format='json')
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_admin.status_code, status.HTTP_204_NO_CONTENT)


class ChoiceTest(SetUp, APITestCase):

    def test_get_choices_list(self):
        response_admin = self.admin_client.get(reverse('choices-list'), format='json')
        response_user = self.user_client.get(reverse('choices-list'), format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_choice_detail(self):
        response = self.admin_client.get(reverse('choice-detail', kwargs={'pk': self.choice.pk}), format='json')
        response_user = self.user_client.get(reverse('choice-detail', kwargs={'pk': self.choice.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_choice(self):
        data = {'question': self.question.pk,
                'text': 'тестовый вариант 2'}
        response_admin = self.admin_client.post(reverse('choices-list'), data, format='json')
        response_user = self.user_client.post(reverse('choices-list'), data, format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_choice(self):
        data = {'question': self.question.pk,
                'text': 'изменненый тестовый вариант 2'}
        response_admin = self.admin_client.put(reverse('choice-detail', kwargs={'pk': self.choice.pk}),
                                               data,
                                               format='json')
        response_user = self.user_client.put(reverse('choice-detail', kwargs={'pk': self.choice.pk}),
                                             data,
                                             format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_choice(self):
        response_user = self.user_client.delete(reverse('choice-detail', kwargs={'pk': self.choice.pk}),
                                                format='json')
        response_admin = self.admin_client.delete(reverse('choice-detail', kwargs={'pk': self.choice.pk}),
                                                  format='json')
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_admin.status_code, status.HTTP_204_NO_CONTENT)


class UserTest(SetUp, APITestCase):

    def test_get_user_answer(self):
        response_admin = self.admin_client.get(reverse('user-answers', kwargs={'id': self.admin.pk}), format='json')
        response_admin2 = self.admin_client.get(reverse('user-answers', kwargs={'id': self.user.pk}), format='json')
        response_user = self.user_client.get(reverse('user-answers', kwargs={'id': self.admin.pk}), format='json')
        response_user2 = self.user_client.get(reverse('user-answers', kwargs={'id': self.user.pk}), format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_admin2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_user2.status_code, status.HTTP_200_OK)

    def test_get_anonim_answer(self):
        response_admin = self.admin_client.get(reverse('anonymous-answers',
                                                       kwargs={'id': self.anonim_answer.anonymous_id}),
                                               format='json')
        response_user = self.user_client.get(reverse('anonymous-answers',
                                                     kwargs={'id': self.anonim_answer.anonymous_id}),
                                             format='json')
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertEqual(response_user.status_code, status.HTTP_403_FORBIDDEN)


class AnswerTest(SetUp, APITestCase):

    def test_get_answer(self):
        response = self.user_client.get(reverse('question-answer', kwargs={'survey_id': self.survey.id,
                                                                           'question_id': self.question.id}),
                                        format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_answer(self):
        data1 = {"answer": "тестовый ответ"}
        data2 = {"answer": "test"}
        data3 = {"answer": "wrong_choice"}
        response1 = self.user_client.post(reverse('question-answer', kwargs={'survey_id': self.survey.pk,
                                                                            'question_id': self.question.pk}),
                                         data1,
                                         format='json')
        response2 = self.user_client.post(reverse('question-answer', kwargs={'survey_id': self.survey.pk,
                                                                            'question_id': self.question_choice.pk}),
                                         data2,
                                         format='json')
        response3 = self.user_client.post(reverse('question-answer', kwargs={'survey_id': self.survey.pk,
                                                                            'question_id': self.question_choice.pk}),
                                         data3,
                                         format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
