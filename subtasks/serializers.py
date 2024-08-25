from rest_framework import serializers
from .models import Subtask

class SubtaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subtask
        fields = '__all__'
        extra_kwargs = {'task': {'required': False}}
            
            
    def update(self, instance, validated_data):
        validated_data.pop('task', None)
        return super().update(instance, validated_data)
        