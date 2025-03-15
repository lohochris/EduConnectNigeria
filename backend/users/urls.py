from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, 
    RegisterUserView, 
    admin_dashboard, 
    tutor_dashboard, 
    UserProfileView,  # Updated to use class-based profile view
    logout_view,  
    password_reset_request,  
    password_reset_confirm,  
)

urlpatterns = [
    # Authentication
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', logout_view, name='logout'),  
    path('register/', RegisterUserView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),  # Use CBV for profile view

    # Dashboards
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('tutor-dashboard/', tutor_dashboard, name='tutor_dashboard'),

    # Password Reset
    path('password-reset/request/', password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', password_reset_confirm, name='password_reset_confirm'),
]
