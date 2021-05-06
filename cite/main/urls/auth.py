from django.urls import path
from main.views import auth

app_name = 'auth'
urlpatterns = [
    path('login/', auth.login, name='login'),
    path('verify/', auth.verify, name='verify'),
    # path('logout/', pass, name='logout'),
    # path('signup/', pass, name='signup'),
]
