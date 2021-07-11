from django.contrib import admin
from .models import *


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_at', 'end_at', 'created_at', 'is_active')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('is_active',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type_question', 'survey')
    list_display_links = ('text', 'type_question')
    search_fields = ('text', 'type_question', 'survey')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text')
    list_display_links = ('question', 'text')
    search_fields = ('question', 'text')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'question', 'answer', 'submit_time')
    list_display_links = ('user_id', 'question', 'answer')
    search_fields = ('user_id', 'question', 'answer')


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
