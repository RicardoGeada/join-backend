from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSelfOrReadOnly
from rest_framework.exceptions import PermissionDenied

from .serializers import CustomUserSerializer
from .models import CustomUser

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    
    def create(self, request, *args, **kwargs):
        """
        Prevent users from being created via this ViewSet.
        """
        raise PermissionDenied("Creating new users is not allowed here.")
    
