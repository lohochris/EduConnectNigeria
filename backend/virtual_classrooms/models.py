from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_jitsi_meeting_url

User = get_user_model()

class VirtualClassroom(models.Model):
    PLATFORM_CHOICES = [
        ('jitsi', 'Jitsi'),
        ('zoom', 'Zoom'),
    ]

    title = models.CharField(max_length=255)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    meeting_url = models.URLField(blank=True, null=True)  # URL is optional for now
    start_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Automatically generate Jitsi URL if platform is Jitsi."""
        if self.platform == 'jitsi' and not self.meeting_url:
            self.meeting_url = generate_jitsi_meeting_url(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.platform}"
