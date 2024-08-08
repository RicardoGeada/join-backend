from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSelfOrReadOnly
from rest_framework.exceptions import PermissionDenied

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import CustomUserSerializer , CustomAuthTokenSerializer
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
    
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email
        })