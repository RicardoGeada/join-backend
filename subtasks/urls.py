from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubtaskViewSet

router = DefaultRouter()
router.register(r'subtasks', SubtaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls))
]
