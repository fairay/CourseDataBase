from django.urls import path
from main.views import duty
from logger import view_log

app_name = 'duty'
urlpatterns = [
    path('drivers/', view_log(duty.drivers), name='drivers'),
    path('drivers/me/', view_log(duty.my_drivers), name='my_drivers'),
    path('drivers/add', view_log(duty.add_driver_duty), name='add_driver'),
    path('guards/', view_log(duty.guards), name='guards'),
    path('guards/add', view_log(duty.add_guard_duty), name='add_guard'),
]
