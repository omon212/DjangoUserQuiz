from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Subject, Question, UserQuizResult, AnswerOption
from .serializers import SubjectSerializer, QuestionSerializer, SubmitQuizSerializer
import random


class SubjectListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=200)


class QuizQuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": "Fan topilmadi"}, status=404)

        questions = list(subject.questions.all())
        random.shuffle(questions)
        selected_questions = questions[:10]

        serializer = QuestionSerializer(selected_questions, many=True)
        return Response(serializer.data, status=200)


class SubmitQuizAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmitQuizSerializer

    def post(self, request, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": "Fan topilmadi"}, status=404)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers = serializer.validated_data['answers']
        score = 0

        for ans in answers:
            try:
                question = Question.objects.get(id=ans["question"])
                option = AnswerOption.objects.get(id=ans["answer"], question=question)

                if option.text.strip().lower() == question.correct_answer.strip().lower():
                    score += 1
            except (Question.DoesNotExist, AnswerOption.DoesNotExist):
                continue

        UserQuizResult.objects.create(
            user=request.user,
            subject=subject,
            score=score,
            total_questions=len(answers)
        )

        return Response({
            "message": "Natija saqlandi",
            "score": score,
            "total_questions": len(answers)
        }, status=status.HTTP_200_OK)
