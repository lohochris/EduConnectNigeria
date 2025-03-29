from django.db import models
from django.contrib.auth import get_user_model  
from django.conf import settings

User = get_user_model()  # Get the custom user model dynamically

# Forum Post Model
class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Indexed for performance
    updated_at = models.DateTimeField(auto_now=True)  # Track updates

    class Meta:
        verbose_name_plural = "Forum Posts"  # Correct plural form
        ordering = ['-created_at']  # Show newest posts first

    def __str__(self):
        user_name = self.user.get_full_name() or self.user.email
        return f"{self.title} by {user_name}"
