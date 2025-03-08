from django.db import models
from users.models import User  # Import User model
from courses.models import Course  # Import Course model

# Progress Tracking
class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_lessons = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
