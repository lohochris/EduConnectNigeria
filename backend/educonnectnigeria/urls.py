from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Redirect root URL to API
def redirect_to_api(request):
    return redirect("api-root")

# API Root View
@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "auth": request.build_absolute_uri("auth/"),
        "token": request.build_absolute_uri("token/"),
        "token_refresh": request.build_absolute_uri("token/refresh/"),
        "token_verify": request.build_absolute_uri("token/verify/"),
        "virtual-classrooms": request.build_absolute_uri("virtual-classrooms/"),
        "assessments": request.build_absolute_uri("assessments/"),
        "ai": request.build_absolute_uri("ai/"),
        "courses": request.build_absolute_uri("courses/"),  # This will now resolve correctly
        "forums": request.build_absolute_uri("forums/"),
    })

urlpatterns = [
    path("", redirect_to_api),  # Redirect root URL to API root
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),  # Set up API root
    path("api/auth/", include("users.urls")),  
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/virtual-classrooms/", include("virtual_classrooms.urls")),
    path("api/assessments/", include("assessments.urls")), 
    path("api/ai/", include("ai_solver.urls")), 
    path("api/", include("courses.urls")),  # 🔹 Include courses directly under "api/"
    path("api/forums/", include("forums.urls")),  
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
