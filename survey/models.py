from django.db import models
from django.contrib.auth import get_user_model


class Survey(models.Model):
    """Опрос пользователей"""

    name = models.CharField(max_length=255, verbose_name='Название опроса')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    start_at = models.DateTimeField(verbose_name='Дата начала опроса')
    end_at = models.DateTimeField(verbose_name='Дата окончания опроса', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['-created_at']


class Question(models.Model):
    """Вопрос для опросов"""

    TYPE = (
        ('text', 'Текст'),
        ('choice', 'Один вариант ответа'),
        ('multi_choice', 'Несколько вариантов ответов')
    )

    text = models.TextField(max_length=2000, verbose_name='Текст вопроса')
    type_question = models.CharField(max_length=50, choices=TYPE, verbose_name='Тип вопроса')
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, verbose_name='Выбрать опрос', related_name='questions')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-survey']


class Choice(models.Model):
    """Вариант выбора для вопроса"""

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=400)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'
        ordering = ['-question']


class Answer(models.Model):
    """Ответ на вопрос"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    anonymous_id = models.IntegerField(blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=1000, verbose_name='Ответ')
    submit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-submit_time']
        unique_together = ['answer', 'question', 'user', 'anonymous_id']