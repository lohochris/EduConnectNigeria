from django.db import models
from users.models import User  # Import User model

# Tutoring Session Model
class TutoringSession(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutoring_sessions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_sessions')
    scheduled_time = models.DateTimeField()
    session_link = models.URLField()
