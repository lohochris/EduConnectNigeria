from django.contrib import admin
from .models import UserQuery, AISolution, QueryFeedback

@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "created_at")

@admin.register(AISolution)
class AISolutionAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "created_at")

@admin.register(QueryFeedback)
class QueryFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "rating", "created_at")
