from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsSelfOrReadOnly
from rest_framework.exceptions import PermissionDenied

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import TokenAuthentication

from .serializers import CustomUserSerializer , CustomAuthTokenSerializer, RegisterSerializer
from .models import CustomUser
from rest_framework import status

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on CustomUser instances.

    Provides standard CRUD operations with token authentication.
    Only authenticated users can edit own user data and read other user data.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]
    authentication_classes = [TokenAuthentication]
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    
    def create(self, request, *args, **kwargs):
        """
        Prevent users from being created via this ViewSet.
        """
        raise PermissionDenied("Creating new users is not allowed here.")
    
    
class LoginView(ObtainAuthToken):
    """
    View for handling user authentication and token generation.

    Inherits from ObtainAuthToken to handle token-based authentication.

    Methods:
        post(request, *args, **kwargs):
            Authenticates the user with the provided credentials and returns a token.
            - If authentication is successful, returns user ID, token, and email.
            - If authentication fails, raises a validation error.
    """
    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id' : user.id,
            'token': token.key,
            'email': user.email
        })
        

class RegisterView(CreateAPIView):
    """
    View for user registration.

    Provides an endpoint for creating new user accounts.

    Permissions:
        - `AllowAny`: Allows any user (authenticated or not) to access this endpoint.

    Methods:
        post(request):
            Registers a new user with the provided data.
            - If the registration is successful, returns a success message.
            - If registration fails (e.g., validation errors), returns error details.
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User successfully registered"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)