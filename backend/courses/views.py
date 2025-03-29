from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied  
from django.shortcuts import get_object_or_404
from .models import Course, LearningMaterial, Enrollment
from .serializers import CourseSerializer, LearningMaterialSerializer, EnrollmentSerializer

class IsInstructor(permissions.BasePermission):
    """
    Custom permission to allow only instructors to create, update, or delete courses.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff  # Assuming instructors are staff

    def has_object_permission(self, request, view, obj):
        return obj.instructor == request.user

# ✅ Course ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)  # Assign course to instructor

# ✅ LearningMaterial ViewSet
class LearningMaterialViewSet(viewsets.ModelViewSet):
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

# ✅ Enrollment ViewSet
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        student = self.request.user
        course = serializer.validated_data['course']

        if Enrollment.objects.filter(student=student, course=course).exists():
            raise PermissionDenied("You are already enrolled in this course.")

        serializer.save(student=student)

# ✅ Student & Instructor Course ViewSets
class StudentEnrolledCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(enrollment__student=self.request.user)

class InstructorCoursesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInstructor]

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)
