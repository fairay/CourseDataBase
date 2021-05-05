from django.urls import include, path
from . import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.home, name='login'),
    path('verify/', views.verify, name='verify'),
]
