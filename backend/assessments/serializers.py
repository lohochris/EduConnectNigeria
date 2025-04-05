from rest_framework import serializers
from .models import Quiz, Question, UserResponse, UserQuizSession

# Quiz Serializer with question count and time limit
class QuizSerializer(serializers.ModelSerializer):
    total_questions = serializers.SerializerMethodField()
    time_limit = serializers.IntegerField()  

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_total_questions(self, obj):
        """Returns the total number of questions in a quiz."""
        return obj.questions.count()

# Question Serializer
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

# User Quiz Session Serializer
class UserQuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizSession
        fields = ['user', 'quiz', 'started_at', 'completed']

# User Response Serializer with validation
class UserResponseSerializer(serializers.ModelSerializer):
    is_correct = serializers.SerializerMethodField()
    quiz_id = serializers.IntegerField(source="quiz.id", read_only=True)  # Include quiz ID for reference

    class Meta:
        model = UserResponse
        fields = '__all__'

    def get_is_correct(self, obj):
        """Checks if the selected option is the correct answer."""
        return obj.selected_option == obj.question.correct_answer

    def validate(self, data):
        """Prevent duplicate responses to the same question by a user."""
        user = self.context['request'].user
        question = data.get('question')

        if UserResponse.objects.filter(user=user, question=question).exists():
            raise serializers.ValidationError("You have already answered this question.")
        
        return data

# Serializer for handling randomized questions
class RandomizedQuizSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    time_limit = serializers.IntegerField()  

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions', 'time_limit']

    def get_questions(self, obj):
        """Returns randomized questions for a quiz."""
        import random
        questions = list(obj.questions.all())
        random.shuffle(questions)
        return QuestionSerializer(questions, many=True).data

# Serializer for automated scoring
class QuizScoreSerializer(serializers.Serializer):
    user = serializers.CharField(source="user.email", read_only=True)
    quiz = serializers.CharField(source="quiz.title", read_only=True)
    score = serializers.FloatField()
    total_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
