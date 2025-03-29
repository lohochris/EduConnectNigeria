from django.db import models
from django.contrib.auth import get_user_model  # Dynamically get the user model
from django.conf import settings

User = get_user_model()  # Get custom user model dynamically
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# Course Model
class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)  # Ensure unique course titles
    description = models.TextField()
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Track updates

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        instructor_name = self.instructor.get_full_name() or self.instructor.email
        return f"{self.title} (Instructor: {instructor_name})"

# Course Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Ensure a student can't enroll in the same course twice
        ordering = ['-enrolled_at']  # Show latest enrollments first

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

# Learning Material Model
class LearningMaterial(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='educonnectnigeria_learning_materials/', blank=True, null=True)  
    content_type = models.CharField(
        max_length=50,
        choices=CONTENT_TYPE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Track updates

    class Meta:
        verbose_name_plural = "Learning Materials"

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"
