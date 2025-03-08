from django.db import models
from users.models import User  # Import the User model

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)

# Learning Material Model
class LearningMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='educonnectnigeria_learning_materials/')
    content_type = models.CharField(max_length=50, choices=[('pdf', 'PDF'), ('video', 'Video'), ('other', 'Other')])
