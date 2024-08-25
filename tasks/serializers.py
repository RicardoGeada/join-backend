from rest_framework import serializers
from .models import Task
from contacts.models import Contact
from subtasks.serializers import SubtaskSerializer
from subtasks.models import Subtask
from django.db import transaction

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model, converting instances to/from JSON.

    Attributes:
        assigned_to (PrimaryKeyRelatedField): Optional field for associating multiple Contacts with the Task.
        subtasks (SubtaskSerializer): Optional field for managing nested Subtasks.

    Methods:
        create(validated_data): Creates a new Task instance and associated Subtasks.
        update(instance, validated_data): Updates an existing Task instance and associated Subtasks.
    """
    
    
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset = Contact.objects.all(),
        many = True,
        required = False
    )
    
    subtasks = SubtaskSerializer(many=True, required=False)
    
    class Meta:
        model = Task
        fields = '__all__'
        
    def create(self, validated_data):
        """
        Create a new Task instance, including nested Subtasks.
        """
        
        assigned_to_data = validated_data.pop('assigned_to', [])
        subtasks_data = validated_data.pop('subtasks', [])
        
        with transaction.atomic():
            # Create the Task instance
            task = Task.objects.create(**validated_data)
            
            # Assign Contacts to the Task
            if assigned_to_data:
                task.assigned_to.set(assigned_to_data)
            
            # Create nested Subtasks
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=task, **subtask_data)
        
        return task
    
    
    
    def update(self, instance, validated_data):
        """
        Update an existing Task instance and its associated Subtasks.
        """
        
        assigned_to_data = validated_data.pop('assigned_to', [])
        subtasks_data = validated_data.pop('subtasks', [])
    
        with transaction.atomic():
            # Update the Task instance
            instance = super().update(instance, validated_data)

            # Update assigned Contacts
            if assigned_to_data:
                instance.assigned_to.set(assigned_to_data) 
        
            # Replace existing Subtasks
            instance.subtasks.all().delete()
            for subtask_data in subtasks_data:
                subtask_data['task'] = instance
                Subtask.objects.create(**subtask_data)
    
        return instance