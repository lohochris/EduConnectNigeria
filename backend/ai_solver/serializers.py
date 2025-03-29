from rest_framework import serializers
from .models import UserQuery, AISolution, QueryFeedback

class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuery
        fields = "__all__"

class AISolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AISolution
        fields = "__all__"

class QueryFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryFeedback
        fields = "__all__"
