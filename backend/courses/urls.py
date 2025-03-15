from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, LearningMaterialListCreateView, LearningMaterialDetailView,
    EnrollmentView, StudentEnrolledCoursesView, InstructorCoursesView
)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/materials/', LearningMaterialListCreateView.as_view(), name='learning-materials'),
    path('materials/<int:pk>/', LearningMaterialDetailView.as_view(), name='learning-material-detail'),
    
    # Enrollment URLs
    path('enroll/', EnrollmentView.as_view(), name='course-enroll'),
    path('my-courses/', StudentEnrolledCoursesView.as_view(), name='student-courses'),
    path('instructor-courses/', InstructorCoursesView.as_view(), name='instructor-courses'),
]
