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
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User successfully registered"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)