from django.db import models
from django.contrib.auth import get_user_model  

User = get_user_model()  # Dynamically fetch the custom User model

class Progress(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='progress', db_index=True
    )
    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="progress", db_index=True
    )
    completed_lessons = models.PositiveIntegerField(default=0)
    total_lessons = models.PositiveIntegerField(default=1)  # Prevents division by zero
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Progress Records"
        unique_together = ('student', 'course')  # Ensures each student has one progress per course
        ordering = ['-last_accessed']
        constraints = [
            models.CheckConstraint(
                check=models.Q(completed_lessons__lte=models.F('total_lessons')),
                name="completed_lessons_lte_total_lessons",
            )
        ]

    def __str__(self):
        return f"{self.student.email} - {self.course.title} ({self.get_progress()}% completed)"

    def get_progress(self):
        """Calculate progress percentage."""
        if self.total_lessons == 0:
            return 0
        progress = (self.completed_lessons / self.total_lessons) * 100
        return min(round(progress, 2), 100)  # Ensure it never exceeds 100%
