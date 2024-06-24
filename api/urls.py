from django.urls import path
from .views import TaskMixinView, collab_task_view

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("auth/", obtain_auth_token),
    path("task/", TaskMixinView.as_view(), name="api"),
    path("task/<int:pk>/", TaskMixinView.as_view(), name="getter"),
    path("task/collab/", collab_task_view, name="collab"),
    path("task/collab/<int:pk>/", collab_task_view, name="one_collab")
]