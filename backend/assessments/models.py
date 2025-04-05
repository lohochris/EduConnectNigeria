from django.db import models
from django.conf import settings
from django.utils.timezone import now
from courses.models import Course

# Quiz Model
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    time_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Time limit in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.title} - {self.course.title}"

    def calculate_score(self, user):
        """Calculate the percentage score based on correct answers."""
        correct_responses = self.questions.filter(
            user_responses__user=user, 
            user_responses__selected_option=models.F('correct_answer')
        ).count()
        total_questions = self.questions.count()
        return (correct_responses / total_questions * 100) if total_questions > 0 else 0

    def has_active_session(self, user):
        """Check if the user has an active, unexpired quiz session."""
        active_session = self.user_sessions.filter(user=user, completed=False).first()
        return active_session and not active_session.has_time_expired()


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    choices = models.JSONField(default=list)  # Stores multiple-choice options

    class Meta:
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"Question: {self.text[:50]}..."

    def is_valid_choice(self, choice):
        """Check if a given choice is one of the available options."""
        return isinstance(self.choices, list) and choice in self.choices


# User Quiz Session Model
class UserQuizSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_sessions')
    started_at = models.DateTimeField(default=now)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'quiz')  # Ensure only one session per user per quiz

    def has_time_expired(self):
        """Check if the quiz time limit has expired."""
        if self.quiz.time_limit:
            elapsed_time = (now() - self.started_at).total_seconds() / 60
            return elapsed_time > self.quiz.time_limit
        return False

    def mark_completed(self):
        """Mark the quiz session as completed."""
        self.completed = True
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} (Started: {self.started_at})"
        return f"{self.user.email} - {self.question.text[:30]}..."



# User Response Model
class UserResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(UserQuizSession, on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_responses')
    selected_option = models.CharField(max_length=255, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'question')  # Ensures one response per question per session

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}..."

    def is_correct(self):
        """Check if the selected option is correct."""
        return self.selected_option == self.question.correct_answer

    def is_within_time_limit(self):
        """Check if the response was submitted within the allowed quiz time."""
        return self.session and not self.session.has_time_expired()
