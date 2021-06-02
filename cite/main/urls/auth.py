from django.urls import path
from main.views import auth
from logger import view_log

app_name = 'auth'
urlpatterns = [
    path('login/', view_log(auth.login), name='login'),
    path('verify/', view_log(auth.verify), name='verify'),
    path('logout/', view_log(auth.logout), name='logout'),
    path('signup/', view_log(auth.signup), name='signup'),
    path('register/', view_log(auth.register), name='register'),
    path('upd_type/', view_log(auth.upd_type), name='upd_type'),
]
