from django.urls import path
from main.views import auth

app_name = 'auth'
urlpatterns = [
    path('login/', auth.login, name='login'),
    path('verify/', auth.verify, name='verify'),
    path('logout/', auth.logout, name='logout'),
    path('signup/', auth.signup, name='signup'),
    path('register/', auth.register, name='register'),
    path('upd_type/', auth.upd_type, name='upd_type')
]
