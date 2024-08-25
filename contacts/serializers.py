from rest_framework import serializers
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model, converting instances to/from JSON.

    Read-only fields:
        - id: Auto-generated unique identifier.
        - initials: Generated from the name.
        - badge_color: Assigned at creation.
        - active_user: Associated user, if any.
    """
    class Meta:
        model = Contact
        fields = ['id', 'name', 'initials', 'email', 'phone', 'badge_color', 'active_user']
        extra_kwargs = {
            'id' : {'read_only' : True},
            'active_user' : {'read_only' : True},
            'initials' : {'read_only' : True},
            'badge_color' : {'read_only' : True},
            }
