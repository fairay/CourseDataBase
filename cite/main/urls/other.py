from django.urls import path
from main.views import other

app_name = 'other'
urlpatterns = [
    path('trucks/', other.trucks, name='trucks'),
    path('add_truck/', other.add_truck, name='add_truck')
]
