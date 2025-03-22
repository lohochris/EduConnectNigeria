from celery import shared_task
from django.utils.timezone import now
from .models import UserQuizSession, UserResponse, Question

@shared_task
def auto_submit_quiz(user_id, quiz_id):
    """Automatically submit all unanswered questions for a user when time expires."""
    session = UserQuizSession.objects.filter(user_id=user_id, quiz_id=quiz_id, completed=False).first()
    
    if session and session.has_time_expired():
        unanswered_questions = Question.objects.filter(quiz_id=quiz_id).exclude(
            id__in=UserResponse.objects.filter(user_id=user_id).values_list('question_id', flat=True)
        )

        for question in unanswered_questions:
            UserResponse.objects.create(
                user_id=user_id,
                question=question,
                selected_option=None  # No answer submitted
            )

        session.completed = True
        session.save()

        print(f"Auto-submitted quiz for user {user_id}")

    return "Quiz auto-submission complete."
