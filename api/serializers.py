from rest_framework import serializers
from .models import TaskModel, SubTaskModel, CollaboratorModel

import api.validators as validators


class CollaboratorSerializer(serializers.ModelSerializer):

    username = serializers.CharField(validators=[validators.validate_username])

    class Meta:
        model = CollaboratorModel
        fields = ['username', 'task']


class SubTaskSerializer(serializers.ModelSerializer):

    status = serializers.CharField(validators=[validators.validate_status])
    due_date = serializers.DateField(validators=[validators.validate_due_date], required=False, read_only=True)
    assigned_to = serializers.CharField(validators=[validators.validate_assigned_to], read_only=True)
    task = serializers.CharField(required=False)

    class Meta:
        model = SubTaskModel
        fields = ['id', 'task', 'title', 'status', 'due_date', 'assigned_to']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('task', None)
        return representation


class TaskModelSerializer(serializers.ModelSerializer):

    subtasks = SubTaskSerializer(many=True, source='subtasks.all', read_only=True)
    status = serializers.CharField(validators=[validators.validate_status])
    due_date = serializers.DateField(validators=[validators.validate_due_date], required=False)
    user = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    task_owner = serializers.CharField(source='user.username', read_only=True)
    collaborators = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TaskModel
        fields = ['id', 'user', 'title', 'status', 'due_date', 'collaborators', 'task_owner', 'subtasks']

    def get_collaborators(self, data):
        collaborators = CollaboratorModel.objects.filter(task=data)
        return collaborators.values_list('username', flat=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user', None)
        return representation
 


