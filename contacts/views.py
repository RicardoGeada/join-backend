from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from .serializers import ContactSerializer
from .models import Contact
from .permissions import IsOwnContactOrNoUserContact

# Create your views here.
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwnContactOrNoUserContact]
    authentication_classes = [TokenAuthentication]