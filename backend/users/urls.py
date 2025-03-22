from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    CustomTokenObtainPairView, 
    RegisterUserView, 
    LogoutView,  # Updated logout to CBV
    UserProfileView, 
    admin_dashboard, 
    tutor_dashboard,  
    password_reset_request,  
    password_reset_confirm,  
)

urlpatterns = [
    # Authentication Endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Verify token
    path('register/', RegisterUserView.as_view(), name='register'),  # User Registration
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout View (CBV)

    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),  

    # Dashboards
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('tutor-dashboard/', tutor_dashboard, name='tutor_dashboard'),

    # Password Reset
    path('password-reset/request/', password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', password_reset_confirm, name='password_reset_confirm'),
]
