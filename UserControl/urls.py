from django.urls import path,include
from .views import *

urlpatterns = [
    path('users/register/',UserRegistraion.as_view(),name='registraion'),
    path('users/login/',Login.as_view(),name='login'),
    path('users/profile/',UserProfile.as_view(),name='Profile'),
]