from django.urls import path
from .views import hello_world, UserLoginAPIView

urlpatterns = [
    path('hello', hello_world),
    path('login', UserLoginAPIView.as_view(), name='login'),
]
