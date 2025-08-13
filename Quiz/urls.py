from django.urls import path
from .views import SubjectListAPIView, QuizQuestionsAPIView, SubmitQuizAPIView

urlpatterns = [
    path("subjects/", SubjectListAPIView.as_view(), name="subject-list"),
    path("<int:subject_id>/questions/", QuizQuestionsAPIView.as_view(), name="quiz-questions"),
    path("<int:subject_id>/submit/", SubmitQuizAPIView.as_view(), name="submit-quiz"),
]