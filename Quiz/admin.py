# Quiz/admin.py
from django.contrib import admin
from .models import Subject, Question, AnswerOption, UserQuizResult


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "subject", "correct_answer")
    list_filter = ("subject",)
    search_fields = ("text",)
    inlines = [AnswerOptionInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(UserQuizResult)
class UserQuizResultAdmin(admin.ModelAdmin):
    list_display = ("user", "subject", "score", "total_questions", "created_at")
    list_filter = ("subject", "created_at")
    search_fields = ("user__username", "subject__name")
    readonly_fields = ("user", "subject", "score", "total_questions", "created_at")


admin.site.register(AnswerOption)