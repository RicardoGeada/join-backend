from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Subtask
from .serializers import SubtaskSerializer

# Create your views here.
class SubtaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Subtask instances.

    Provides standard CRUD operations with token authentication.
    Only authenticated users can modify subtasks.
    """
    
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    