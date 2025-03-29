from django.urls import path
from .views import AIQuestionSolver

urlpatterns = [
    path('solve/', AIQuestionSolver.as_view(), name='ai-question-solver'),
]
