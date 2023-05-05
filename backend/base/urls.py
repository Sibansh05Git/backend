from django.contrib import admin
from django.urls import path,include
from . import views
from base.views import *

urlpatterns = [
    path("crop_recommendation/",views.crop_recommendation,name="crop_recommendation"),
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
