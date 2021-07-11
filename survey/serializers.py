from rest_framework import serializers
import datetime

from .models import Survey, Question, Choice, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    """Создание варианта ответа"""

    class Meta:
        model = Choice
        fields = ['url', 'text', 'question']


class QuestionForUserSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор для сериализатора ответа"""

    choices = serializers.SlugRelatedField(slug_field='text', read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('survey', 'id', 'text', 'type_question', 'choices')
        read_only_fields = ('id',)


class AnswerSerializer(serializers.Serializer):
    """Ввод ответа на конкретный вопрос"""

    user = serializers.IntegerField(write_only=True, required=False)
    poll = serializers.CharField(max_length=500, read_only=True)
    question = serializers.CharField(max_length=500, read_only=True)
    type_question = serializers.ChoiceField(choices=Question.TYPE, read_only=True)
    choices = serializers.ListField(read_only=True)
    answer = serializers.CharField(max_length=300, required=True)

    def validate_answer(self, value):
        question = Question.objects.get(pk=self.context['question_id'])
        type_question = question.type_question
        choices = [q.text for q in question.choices.all()]
        if type_question in ('choice', 'multi_choice'):
            if type_question == 'choice':
                if value not in choices:
                    raise serializers.ValidationError("Вы ввели недопустимый ответ")
            elif type_question == 'multi_choice':
                answers = value.split(',')
                for answer in answers:
                    if answer not in choices:
                        raise serializers.ValidationError("Вы ввели недопустимый ответ")
        return value

    def save(self, question, user=None):
        answer = self.validated_data['answer']
        if user:
            return Answer.objects.create(user_id=user, question_id=question, answer=answer)
        elif self.validated_data.get('user'):
            return Answer.objects.create(anonymous_id=self.validated_data['user'],
                                         question_id=question,
                                         answer=answer)

class QuestionSerializer(serializers.ModelSerializer):
    """Вопрос"""

    choices = serializers.SlugRelatedField(slug_field='text', read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('url', 'id', 'text', 'type_question', 'choices')
        read_only_fields = ('id',)


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Создание вопроса"""

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('id',)


class SurveyListSerializer(serializers.HyperlinkedModelSerializer):
    """Список всех опросов"""

    class Meta:
        model = Survey
        fields = ('url', 'id', 'name')
        read_only_fields = ('id',)


class SurveyDetailSerializer(serializers.ModelSerializer):
    """Детальная информация по опросу"""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ('name', 'description', 'end_at', 'created_at', 'questions')
        read_only_fields = ('id', 'start_at')


class SurveyCreateSerializer(serializers.ModelSerializer):
    """Создание опроса"""

    def validate(self, data):
        if data['start_at'] > data['end_at']:
            raise serializers.ValidationError("Дата окончания не может быть раньше даты начала")
        if data['end_at'] < datetime.datetime.today():
            raise serializers.ValidationError("Дата окончания не может быть меньше текущей даты")
        return data

    class Meta:
        model = Survey
        fields = '__all__'
        read_only_fields = ('id',)


class UserAnswerSerializer(serializers.ModelSerializer):
    """Ответы пользователя"""

    question = QuestionForUserSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ['user', 'question', 'answer']
        read_only_fields = ('id', 'question', 'user')
