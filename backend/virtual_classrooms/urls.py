from django.urls import path
from .views import (
    VirtualClassroomListCreateView,
    VirtualClassroomDetailView,
    ZoomOAuthLoginView,
    ZoomOAuthCallbackView,
    CreateZoomMeetingView,
    api_root  # Import the API root view
)

urlpatterns = [
    path('', api_root, name='api-root'),  # Register API Root
    path('virtual-classrooms/', VirtualClassroomListCreateView.as_view(), name="virtual-classroom-list"),
    path('virtual-classrooms/<int:pk>/', VirtualClassroomDetailView.as_view(), name="virtual-classroom-detail"),
    path('virtual-classrooms/zoom/login/', ZoomOAuthLoginView.as_view(), name="zoom-oauth-login"),
    path('virtual-classrooms/zoom/callback/', ZoomOAuthCallbackView.as_view(), name="zoom-oauth-callback"),
    path('virtual-classrooms/zoom/create-meeting/', CreateZoomMeetingView.as_view(), name="create-zoom-meeting"),
]
