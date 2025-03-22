from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
import requests
import os
from dotenv import load_dotenv
from .models import VirtualClassroom
from .serializers import VirtualClassroomSerializer

# Load environment variables
load_dotenv()

# Zoom OAuth Credentials
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")
ZOOM_REDIRECT_URI = "http://localhost:8000/api/virtual-classrooms/zoom/callback/"
ZOOM_AUTH_URL = "https://zoom.us/oauth/authorize"
ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"

class VirtualClassroomListCreateView(generics.ListCreateAPIView):
    """API to create and list virtual classrooms"""
    queryset = VirtualClassroom.objects.all()
    serializer_class = VirtualClassroomSerializer
    permission_classes = [IsAuthenticated]

class VirtualClassroomDetailView(generics.RetrieveDestroyAPIView):
    """API to get details of a virtual classroom"""
    queryset = VirtualClassroom.objects.all()
    serializer_class = VirtualClassroomSerializer
    permission_classes = [IsAuthenticated]

class ZoomOAuthLoginView(View):
    """Handles Zoom OAuth login redirect"""
    def get(self, request, *args, **kwargs):
        auth_url = f"{ZOOM_AUTH_URL}?response_type=code&client_id={ZOOM_CLIENT_ID}&redirect_uri={ZOOM_REDIRECT_URI}"
        return redirect(auth_url)

class ZoomOAuthCallbackView(View):
    """Handles Zoom OAuth callback and exchanges code for access token"""
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No code received from Zoom"}, status=400)
        
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": ZOOM_REDIRECT_URI,
        }
        
        headers = {
            "Authorization": f"Basic {ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        
        response = requests.post(ZOOM_TOKEN_URL, data=token_data, headers=headers)
        token_response = response.json()
        
        if "access_token" in token_response:
            return JsonResponse(token_response)
        else:
            return JsonResponse(token_response, status=400)

class CreateZoomMeetingView(View):
    """Handles creating a Zoom meeting via API"""
    def get(self, request, *args, **kwargs):
        access_token = request.GET.get("access_token")  # Use stored token in real cases

        if not access_token:
            return JsonResponse({"error": "Access token is required"}, status=400)

        meeting_data = {
            "topic": "EduConnect Virtual Class",
            "type": 2,
            "start_time": "2024-03-21T15:00:00Z",
            "duration": 60,
            "timezone": "UTC",
            "agenda": "Online Learning Session",
            "settings": {
                "host_video": True,
                "participant_video": True,
                "mute_upon_entry": True,
            },
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        response = requests.post("https://api.zoom.us/v2/users/me/meetings", json=meeting_data, headers=headers)
        return JsonResponse(response.json())

# API Root View
def api_root(request):
    """API Root Endpoint"""
    return JsonResponse({
        "virtual_classrooms": request.build_absolute_uri(reverse("virtual-classroom-list")),
        "auth": request.build_absolute_uri(reverse("token_obtain_pair")),
        "assessments": request.build_absolute_uri(reverse("assessments-list")),  # Adjust if necessary
    })
