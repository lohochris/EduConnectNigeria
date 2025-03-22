from django.urls import path
from .views import (
    QuizListView, 
    QuizDetailView, 
    QuestionListView, 
    SubmitResponseView,
    QuizScoreView,  
    StartQuizView
)

urlpatterns = [
    path("", QuizListView.as_view(), name="assessments-list"),  # API root listing all quizzes
    path("quizzes/", QuizListView.as_view(), name="quiz-list"),  # List all quizzes
    path("quizzes/<int:quiz_id>/start/", StartQuizView.as_view(), name="quiz-start"),  # Start quiz session
    path("quizzes/<int:quiz_id>/", QuizDetailView.as_view(), name="quiz-detail"),  # Fetch single quiz details
    path("quizzes/<int:quiz_id>/questions/", QuestionListView.as_view(), name="quiz-questions"),  # Fetch quiz questions
    path("quizzes/<int:quiz_id>/submit/", SubmitResponseView.as_view(), name="submit-response"),  # Submit user response
    path("quizzes/<int:quiz_id>/score/", QuizScoreView.as_view(), name="quiz-score"),  # Fetch quiz score
]
