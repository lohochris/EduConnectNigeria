from rest_framework import serializers
from .models import VirtualClassroom

class VirtualClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualClassroom
        fields = "__all__"
