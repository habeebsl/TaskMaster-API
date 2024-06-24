from django.shortcuts import render
from rest_framework import generics, mixins, filters, authentication

from .models import TaskModel, SubTaskModel, CollaboratorModel
from .serializers import TaskModelSerializer, SubTaskSerializer, CollaboratorSerializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

class TaskMixinView(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,          
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView
                ):
    
    queryset = TaskModel.objects.all()
    serializer_class = TaskModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'status', 'due_date', 'id']

    def perform_create(self, serializer):
        requested_data = self.request.data
        sub_tasks = requested_data.get('subtasks', [])
        collaborators = requested_data.get('collaborators', [])

        if requested_data.get("id", None) != None:
            raise serializers.ValidationError("id field is invalid, please remove it from the request")
        if self.request.user.username in collaborators:
            raise serializers.ValidationError(f"Task Owner - '{self.request.user.username}' cannot be a collaborator")
        
        print(f"Authenticated user: {self.request.user}")
        task = serializer.save(user=self.request.user)

        for sub_task in sub_tasks:
            subtask_serializer = SubTaskSerializer(data=sub_task)
            if subtask_serializer.is_valid(raise_exception=True):
                if isinstance(sub_task, dict):
                    SubTaskModel.objects.create(task=task, **sub_task)      
            
        for collaborator in collaborators:
            collaborator_dict = {"username": collaborator, "task":task.id}
            collaborator_serializer = CollaboratorSerializer(data=collaborator_dict)
            if collaborator_serializer.is_valid(raise_exception=True):
                collaborator_serializer.save(task=task)
        return task
    
    def perform_update(self, serializer):
        requested_data = self.request.data
        subtasks_data = requested_data.get('subtasks', [])
        collaborators = requested_data.get('collaborators', [])

        for subtask_data in subtasks_data:
            subtask_serializer = SubTaskSerializer(data=subtask_data)
            subtask_serializer.is_valid(raise_exception=True)

        if self.request.user.username in collaborators:
            raise serializers.ValidationError(f"Task Owner - '{self.request.user.username}' cannot be a collaborator")
        
        task = serializer.save()
        if subtasks_data:
            for subtask_data in subtasks_data:
                subtask_serializer = SubTaskSerializer(data=subtask_data)
                if subtask_serializer.is_valid(raise_exception=True):
                    subtask_id = subtask_data.get('id')
                    if subtask_id:
                        subtask = SubTaskModel.objects.get(id=subtask_id, task=task)
                        subtask.title = subtask_data.get('title', subtask.title)
                        subtask.status = subtask_data.get('status', subtask.status)
                        subtask.due_date = subtask_data.get('due_date', subtask.due_date)
                        subtask.assigned_to = subtask_data.get('assigned_to', subtask.assigned_to)
                        subtask.save()
                    else:
                        SubTaskModel.objects.create(task=task, **subtask_data)
        
        
        if collaborators:
            CollaboratorModel.objects.filter(task=task).delete()
            for collaborator in collaborators:
                collaborator_dict = {"username": collaborator, "task":task.id}
                collaborator_serializer = CollaboratorSerializer(data=collaborator_dict)
                if collaborator_serializer.is_valid(raise_exception=True):
                    collaborator_serializer.save(task=task)

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

@api_view(['GET', 'PUT'])
def collab_task_view(request, pk=None, **kwargs):
    username = request.user.username
    queryset = CollaboratorModel.objects.filter(username=username)
    tasks = [collaborator.task for collaborator in queryset]
    if request.method == 'GET':
        if pk == None:   
            serializer = TaskModelSerializer(tasks, many=True).data
            return Response(serializer)
        else:
            for task in tasks:
                if task.id == pk:
                    serializer = TaskModelSerializer(task).data
                    return Response(serializer)
            return Response({"Task Error": "You are not a collaborator in this task or Task Does not exist"})
    else:
        task_instance = None
        request_data = request.data
        subtasks = request_data.get("subtasks", [])

        for task in tasks:
            if task.id == pk:
                task_instance = task
                serializer = TaskModelSerializer(task).data
                break

        if not task_instance:
            raise serializers.ValidationError("Task not found")

        for subtask in subtasks:
            subtask_id = subtask.get("id")
            assigned_user = subtask.get("assigned_to")
            SubTaskSerializer(data=subtask).is_valid(raise_exception=True)
            if assigned_user == request.user.username:
                model_subtask = SubTaskModel.objects.get(id=subtask_id, task=task_instance)
                model_subtask.status = subtask.get("status")
                model_subtask.save()
            # else:
            #     raise serializers.ValidationError("You connot modify the status of subtasks you were not assigned")

        model_task = TaskModel.objects.get(id=pk)
        serializer = TaskModelSerializer(model_task)

        return Response(serializer.data)



            
            


            
                
            
    
            
    
