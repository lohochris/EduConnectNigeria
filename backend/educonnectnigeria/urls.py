from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

def redirect_to_api(request):
    return redirect("api/")

urlpatterns = [
    path("", redirect_to_api),  # Redirect root URL to API
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),  
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/", include("virtual_classrooms.urls")),
    path("api/assessments/", include("assessments.urls")),  
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
