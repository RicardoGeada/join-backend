from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, LoginView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login')
]