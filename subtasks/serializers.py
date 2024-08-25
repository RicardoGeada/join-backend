from rest_framework import serializers
from .models import Subtask

class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subtask model, converting instances to/from JSON.
    
    Methods:
        update(instance, validated_data): Updates a Subtask instance, excluding 'task' from the update.
    """
    class Meta:
        model = Subtask
        fields = '__all__'
        extra_kwargs = {
            'task': {'required': False}, # not required for nested creation
            }
            
            
    def update(self, instance, validated_data):
        """
        Update the given Subtask instance with the provided validated data.
        
        Args:
            instance (Subtask): The instance to be updated.
            validated_data (dict): Data to update the instance with.
        
        Returns:
            Subtask: The updated Subtask instance.
        """
        validated_data.pop('task', None)  # Remove 'task' from the validated data as it should not be modified
        return super().update(instance, validated_data)
        