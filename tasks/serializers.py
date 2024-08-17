from rest_framework import serializers
from .models import Task
from contacts.models import Contact
from subtasks.serializers import SubtaskSerializer
from subtasks.models import Subtask
from django.db import transaction

class TaskSerializer(serializers.ModelSerializer):
    
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
        assigned_to_data = validated_data.pop('assigned_to', [])
        subtasks_data = validated_data.pop('subtasks', [])
        
        with transaction.atomic():
            task = Task.objects.create(**validated_data)
            
            if assigned_to_data:
                task.assigned_to.set(assigned_to_data)
            
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=task, **subtask_data)
        
        return task
    
    def update(self, instance, validated_data):
        assigned_to_data = validated_data.pop('assigned_to', [])
        subtasks_data = validated_data.pop('subtasks', [])
    
        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if assigned_to_data:
                instance.assigned_to.set(assigned_to_data) 
        
            instance.subtasks.all().delete()
            for subtask_data in subtasks_data:
                subtask_data['task'] = instance
                Subtask.objects.create(**subtask_data)
    
        return instance