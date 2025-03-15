from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()  # Dynamically fetch the custom User model

class TutoringSession(models.Model):
    tutor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tutoring_sessions', db_index=True
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='learning_sessions', db_index=True
    )
    scheduled_time = models.DateTimeField()
    session_link = models.URLField(blank=True, null=True)  # Optional session link
    session_status = models.CharField(
        max_length=20,
        choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Canceled', 'Canceled')],
        default='Scheduled'
    )

    class Meta:
        verbose_name_plural = "Tutoring Sessions"
        ordering = ['scheduled_time']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(tutor=models.F('student')),
                name="tutor_must_not_be_student",
            )
        ]

    def clean(self):
        """Ensure tutor and student are not the same user."""
        if self.tutor == self.student:
            raise ValidationError("A tutor cannot tutor themselves.")

    def __str__(self):
        return f"Tutoring: {self.tutor.email} → {self.student.email} at {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"
