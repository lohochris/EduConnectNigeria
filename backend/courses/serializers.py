from rest_framework import serializers
from .models import Course, LearningMaterial, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.ReadOnlyField(source='instructor.username')
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['instructor'] = request.user
        return super().create(validated_data)

class LearningMaterialSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    content_type_display = serializers.CharField(source='get_content_type_display', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    
    class Meta:
        model = LearningMaterial
        fields = ['id', 'course', 'title', 'file', 'content_type', 'content_type_display', 'created_at', 'updated_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    enrolled_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
