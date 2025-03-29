from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings

class UserQuery(models.Model):
    """Stores user-submitted queries to the AI solver."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()  # The user's math problem or query
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by {self.user.username if self.user else 'Anonymous'} on {self.created_at}"

class AISolution(models.Model):
    """Stores AI-generated solutions to user queries."""
    query = models.OneToOneField(UserQuery, on_delete=models.CASCADE, related_name="solution")
    answer = models.TextField()  # The AI-generated solution
    explanation = models.TextField(null=True, blank=True)  # Optional step-by-step explanation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solution for Query {self.query.id}"

class QueryFeedback(models.Model):
    """Allows users to rate AI-generated solutions."""
    query = models.OneToOneField(UserQuery, on_delete=models.CASCADE, related_name="feedback")
    rating = models.IntegerField(choices=[(1, "Poor"), (2, "Fair"), (3, "Good"), (4, "Very Good"), (5, "Excellent")], default=3)
    comments = models.TextField(null=True, blank=True)  # Optional feedback from the user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Query {self.query.id}: {self.rating} stars"
