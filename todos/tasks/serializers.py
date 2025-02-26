from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'status', 'created_at']
        read_only_fields = ('id', 'user')
