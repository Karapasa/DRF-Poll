from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from TestTask.yasg import urlpatterns as doc_urls
from survey.views import *

admin_methods = {'get': 'retrieve',
                 'put': 'update',
                 'patch': 'partial_update',
                 'delete': 'destroy'}


urlpatterns = [
    path('admin-list/', api_admin_root, name='admin-list'),
    path('surveys/', SurveyView.as_view({'get': 'list', 'post': 'create'}), name='surveys-list'),
    path('surveys/<int:pk>/', SurveyView.as_view(admin_methods), name='survey-detail'),
    path('surveys/<int:survey_id>/<int:question_id>/', AnswerView.as_view(), name='question-answer'),
    path('questions/', QuestionView.as_view({'get': 'list', 'post': 'create'}), name='questions-list'),
    path('questions/<int:pk>/', QuestionView.as_view(admin_methods), name='question-detail'),
    path('choices/', ChoiceView.as_view({'get': 'list', 'post': 'create'}), name='choices-list'),
    path('choices/<int:pk>/', ChoiceView.as_view(admin_methods), name='choice-detail'),
    path('user/<int:id>/', UserView.as_view(), name='user-answers'),
    path('anonim-user/<int:id>/', AnonymousUserView.as_view(), name='anonymous-answers')
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += doc_urls
