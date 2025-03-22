from django.contrib import admin
from .models import Quiz, Question, UserQuizSession, UserResponse

# Inline model for Questions (displayed within QuizAdmin)
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2  # Show 2 empty question slots by default

# Quiz Admin with inline Questions
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'time_limit', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'time_limit')
    inlines = [QuestionInline]  # Show questions within quiz admin

# Question Admin
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'correct_answer')
    search_fields = ('text', 'quiz__title')
    list_filter = ('quiz',)

# User Quiz Session Admin
@admin.register(UserQuizSession)
class UserQuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'started_at', 'completed')
    search_fields = ('user__username', 'quiz__title')
    list_filter = ('completed',)

#  User Response Admin
@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_quiz', 'question', 'selected_option', 'submitted_at')
    search_fields = ('user__username', 'question__text')
    list_filter = ('question__quiz', 'submitted_at')

    def get_quiz(self, obj):
        return obj.question.quiz.title  # Fetch the quiz title
    get_quiz.short_description = 'Quiz'  # Set admin column name
