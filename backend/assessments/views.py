from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Quiz, Question, UserResponse, UserQuizSession
from .serializers import (
    QuizSerializer, QuestionSerializer, UserResponseSerializer, 
    RandomizedQuizSerializer, QuizScoreSerializer
)

# 1. List all quizzes
class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

# 2. Retrieve a specific quiz with randomized questions
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = RandomizedQuizSerializer
    permission_classes = [IsAuthenticated]

# 3. Fetch all questions for a given quiz
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        quiz_id = self.kwargs['quiz_id']
        return Question.objects.filter(quiz_id=quiz_id)

# 4. Start a quiz session (ensures session integrity)
class StartQuizView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        user = request.user
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Check if the user already has an active session
        active_session = UserQuizSession.objects.filter(user=user, quiz=quiz, completed=False).first()
        
        if active_session:
            return Response({
                "message": "You already have an active session!",
                "started_at": active_session.started_at
            }, status=status.HTTP_200_OK)

        # Create a new session
        session = UserQuizSession.objects.create(user=user, quiz=quiz, started_at=now())
        return Response({
            "message": "Quiz started!",
            "started_at": session.started_at
        }, status=status.HTTP_201_CREATED)

# 5. Submit user response with session & time validation
class SubmitResponseView(generics.CreateAPIView):
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        question_id = request.data.get("question")
        selected_option = request.data.get("selected_option")

        question = get_object_or_404(Question, id=question_id)
        quiz = question.quiz

        # Ensure user has an active session
        session = UserQuizSession.objects.filter(user=user, quiz=quiz, completed=False).first()
        if not session:
            return Response({"error": "You have not started this quiz!"}, status=status.HTTP_400_BAD_REQUEST)

        # Enforce time limit
        if session.has_time_expired():
            session.mark_completed()  # Mark session as completed
            return Response({"error": "Time is up! You cannot submit answers anymore."}, status=status.HTTP_403_FORBIDDEN)

        # Ensure user has not already answered this question in the session
        existing_response = UserResponse.objects.filter(user=user, session=session, question=question).first()
        if existing_response:
            return Response({"error": "You have already answered this question."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the answer is correct
        is_correct = selected_option == question.correct_answer

        # Save user response
        UserResponse.objects.create(
            user=user,
            session=session,
            question=question,
            selected_option=selected_option
        )

        return Response({
            "message": "Response submitted!",
            "question": question.text,
            "selected_option": selected_option,
            "is_correct": is_correct
        }, status=status.HTTP_201_CREATED)

# 6. Calculate quiz score for the user's current session
class QuizScoreView(generics.RetrieveAPIView):
    serializer_class = QuizScoreSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, quiz_id):
        user = request.user
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Fetch the user's latest completed session
        session = UserQuizSession.objects.filter(user=user, quiz=quiz, completed=True).order_by('-started_at').first()
        
        if not session:
            return Response({"error": "No completed quiz session found!"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve only responses for this session
        responses = UserResponse.objects.filter(session=session)
        total_questions = quiz.questions.count()
        correct_answers = sum(1 for r in responses if r.selected_option == r.question.correct_answer)
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        return Response({
            "user": user.email,
            "quiz": quiz.title,
            "score": score,
            "total_questions": total_questions,
            "correct_answers": correct_answers
        }, status=status.HTTP_200_OK)
