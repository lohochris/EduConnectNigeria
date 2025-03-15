from django.db import models
from courses.models import Course  # Import Course model

# Quiz Model
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Quizzes"  # Correct plural form in admin panel

    def __str__(self):
        return f"{self.title} - {self.course.title}"  # Display Course title instead of object reference

# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    choices = models.JSONField(default=list)  # Ensures it defaults to an empty list

    class Meta:
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"Question: {self.text[:50]}..."  # Show first 50 characters of the question

    def is_valid_choice(self, choice):
        """Check if a given choice is a valid option for this question."""
        return isinstance(self.choices, list) and choice in self.choices
