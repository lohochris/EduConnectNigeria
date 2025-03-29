from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, LearningMaterialViewSet, EnrollmentViewSet,
    StudentEnrolledCoursesViewSet, InstructorCoursesViewSet
)

# 🔹 Register ViewSets with Router
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'courses/(?P<course_id>\d+)/materials', LearningMaterialViewSet, basename='learning-materials')
router.register(r'enroll', EnrollmentViewSet, basename='enrollment')
router.register(r'my-courses', StudentEnrolledCoursesViewSet, basename='student-courses')
router.register(r'instructor-courses', InstructorCoursesViewSet, basename='instructor-courses')

urlpatterns = [
    path('', include(router.urls)),
]
