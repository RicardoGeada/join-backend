from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from .serializers import ContactSerializer
from .models import Contact
from .permissions import IsOwnContactOrNoUserContact

# Create your views here.
class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Contact instances.

    Provides standard CRUD operations with token authentication.
    Only authenticated users can modify their own contacts or unassigned contacts.
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwnContactOrNoUserContact]
    authentication_classes = [TokenAuthentication]