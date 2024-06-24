from rest_framework import serializers
from datetime import datetime
from django.contrib.auth.models import User
  
def validate_due_date(date):
    if date < datetime.now().date():
        raise serializers.ValidationError("Due date must not be in the past")
    else:
        return date
        
def validate_status(status):
    statuses = ["to-do", "in-progress", "completed"]
    if status not in statuses:
        raise serializers.ValidationError("The status must be one of the following: to-do, in-progress, or completed.")
    else:
        return status

def validate_assigned_to(assigned_user):
    user_exists = User.objects.filter(username=assigned_user).exists()

    if user_exists:
        print("User Exists")
        return assigned_user
    else:
        raise serializers.ValidationError("User does not exist")
    
def validate_username(collaborator):
    user_exists = User.objects.filter(username=collaborator).exists()

    if user_exists:
        print("Collaborator Exists")
        return collaborator
    else:
        raise serializers.ValidationError(f"{collaborator} does not exist")
    