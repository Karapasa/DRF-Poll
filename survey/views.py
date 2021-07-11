from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions, status, filters
from .permissions import CreationOnlyAdmin, IsAuthorAccess
from .serializers import *


@api_view(['GET'])
def api_root(request):
    return Response({'surveys': reverse('surveys-list', request=request),
                     'admin': reverse('admin-list', request=request)
                     })


@api_view(['GET'])
@permission_classes((permissions.IsAdminUser,))
def api_admin_root(request):
    return Response({'choices': reverse('choices-list', request=request),
                     'question': reverse('questions-list', request=request),
                     'surveys': reverse('surveys-list', request=request)})


class SurveyView(viewsets.ModelViewSet):
    """Вывод всех активных опросов и детальный вывод опроса и создание опроса"""

    permission_classes = (CreationOnlyAdmin,)

    def get_queryset(self):
        surveys = Survey.objects.filter(is_active=True)
        return surveys

    def get_serializer_class(self):
        if self.action == 'list':
            return SurveyListSerializer
        elif self.action == 'create':
            return SurveyCreateSerializer
        return SurveyDetailSerializer


class UserView(generics.ListAPIView):
    """Вывод ответов зарегистрированных пользователей"""

    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAdminUser | IsAuthorAccess]

    def get_queryset(self):
        return Answer.objects.filter(user_id=self.kwargs['id'])


class AnonymousUserView(generics.ListAPIView):
    """Вывод ответов анонимных пользователей"""

    serializer_class = UserAnswerSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        return Answer.objects.filter(anonymous_id=self.kwargs['id'])


class ChoiceView(viewsets.ModelViewSet):
    """Вывод вариантов ответа и детальный вывод"""

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['question']
    search_fields = ['text']


class QuestionView(viewsets.ModelViewSet):
    """Вывод вопросов и детальный вывод отдельного вопроса"""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', '=type_question']

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionSerializer
        return QuestionCreateSerializer


class AnswerView(APIView):
    """View для введения ответа на вопрос"""
    def get(self, request, question_id, survey_id):

        obj = Question.objects.get(pk=question_id)
        poll_name = obj.survey.name
        choices = obj.choices.all()
        answer = 'Введите ответ'
        data = {'poll': poll_name,
                'question': obj.text,
                'type_question': obj.type_question,
                'choices': [i.text for i in choices],
                'answer': answer}
        serializer = AnswerSerializer(data, context={"tips": "Подсказка"})
        return Response(serializer.data)

    def post(self, request, survey_id, question_id):
        if self.request.user.is_authenticated:
            request.data['user'] = request.user.pk
        serializer = AnswerSerializer(data=request.data, context={'question_id': question_id})
        if serializer.is_valid(raise_exception=True):
            if self.request.user.is_authenticated:
                serializer.save(user=request.user.pk, question=question_id)
            else:
                serializer.save(question=question_id)
            return Response(status=status.HTTP_201_CREATED)
