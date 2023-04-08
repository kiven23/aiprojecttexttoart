from django.urls import path
from .views import hello_world, UserLoginAPIView, CreateUser

urlpatterns = [
    path('hello', hello_world),
    path('login', UserLoginAPIView.as_view(), name='login'),
    path('register', CreateUser.as_view(), name='register'),
]
