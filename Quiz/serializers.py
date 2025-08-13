from rest_framework import serializers
from .models import Subject, Question, AnswerOption, UserQuizResult


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["id", "text"]


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "options"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name"]


class UserQuizResultSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()

    class Meta:
        model = UserQuizResult
        fields = ["id", "subject", "score", "total_questions", "created_at"]