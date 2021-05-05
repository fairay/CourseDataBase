from django.urls import include, path
from . import views

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from src import *

urlpatterns = [
    path('', views.home),
    path('auth/', views.verify),
]
