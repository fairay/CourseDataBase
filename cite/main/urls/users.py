from django.urls import path
from main.views import users

app_name = 'auth'
urlpatterns = [
    path('profile/', users.my_profile, name='profile'),
    path('profile/<str:login>', users.profile, name='profile'),
    path('users/all/', users.get_all, name='all'),
]
