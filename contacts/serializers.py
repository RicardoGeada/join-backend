from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contact
        fields = ['id', 'name', 'initials', 'email', 'phone', 'badge_color', 'active_user']
        extra_kwargs = {
            'id' : {'read_only' : True},
            'active_user' : {'read_only' : True},
            'initials' : {'read_only' : True},
            'badge_color' : {'read_only' : True},
            }
