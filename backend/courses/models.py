from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get custom user model dynamically

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
        """Return course title and instructor name, fallback to email if necessary."""
        instructor_name = getattr(self.instructor, "get_full_name", lambda: None)()
        if not instructor_name or instructor_name.strip() == "":
            instructor_name = getattr(self.instructor, "email", "Unknown Instructor")  # Fallback to email
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
        return f"{self.student.email} enrolled in {self.course.title}"

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
