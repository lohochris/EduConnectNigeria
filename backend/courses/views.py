from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied  
from django.shortcuts import get_object_or_404
from .models import Course, LearningMaterial
from .serializers import CourseSerializer, LearningMaterialSerializer

class IsInstructor(permissions.BasePermission):
    """
    Custom permission to allow only instructors to create, update, or delete courses.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff  # Assuming instructors are staff

    def has_object_permission(self, request, view, obj):
        return obj.instructor == request.user

# Course Views
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)  # Assign course to instructor

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

# Learning Material Views
class LearningMaterialListCreateView(generics.ListCreateAPIView):
    serializer_class = LearningMaterialSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return LearningMaterial.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        if course.instructor != self.request.user:
            raise PermissionDenied("You can only add materials to your own courses.")
        serializer.save(course=course)

class LearningMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LearningMaterial.objects.all()
    serializer_class = LearningMaterialSerializer
    permission_classes = [IsAuthenticated, IsInstructor]
