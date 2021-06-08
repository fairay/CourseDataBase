from django.urls import path
from main.views import users
from logger import view_log

app_name = 'users'
urlpatterns = [
    path('profile/', view_log(users.my_profile), name='profile'),
    path('profile/<str:login>', view_log(users.profile), name='profile'),
    path('users/all/', view_log(users.get_all), name='all'),
    path('users/unverified/', view_log(users.get_unverified), name='unverified'),
    path('users/approve/<str:login>', view_log(users.approve_user), name='unverified'),
    path('users/delete/<str:login>', view_log(users.del_user), name='del_user'),
]
