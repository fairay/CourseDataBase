from django.urls import path
from .views import auth

app_name = 'auth'
urlpatterns = [
    path('login/', auth.login, name='login'),
    path('verify/', auth.verify, name='verify'),
    path('profile/', auth.profile, name='profile')
]
