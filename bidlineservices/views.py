from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from .models import Project, Tasks
# from .forms import CreateNewTask, CreateNewProject

# Create your views here.
def index(request):
  return HttpResponse(f'<h1>Welcome to Bidline Services</h1>')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})
