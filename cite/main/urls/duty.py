from django.urls import path
from main.views import duty

app_name = 'duty'
urlpatterns = [
    path('drivers/', duty.drivers, name='drivers'),
    path('drivers/add', duty.add_driver_duty, name='add_driver')
]