from django.urls import path
from main.views import users

app_name = 'users'
urlpatterns = [
    path('profile/', users.my_profile, name='profile'),
    path('profile/<str:login>', users.profile, name='profile'),
    path('users/all/', users.get_all, name='all'),
    path('users/unverified/', users.get_unverified, name='unverified'),
    path('users/unverified/<str:login>', users.approve_user, name='unverified')
]
