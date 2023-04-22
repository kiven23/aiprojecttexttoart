from django.urls import path
from .views import hello_world,\
    UserLoginAPIView,\
    CreateUser,\
    Profile, \
    MyBranch

urlpatterns = [
    path('hello', hello_world),
    path('login', UserLoginAPIView.as_view(), name='login'),
    path('register', CreateUser.as_view(), name='register'),
    path('profile', Profile.as_view(), name='profile'),
    # path('pets', Mypet.as_view(), name='post'),
    path('branch', MyBranch.as_view(), name='branches')
]
