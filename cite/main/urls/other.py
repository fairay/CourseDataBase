from django.urls import path
from main.views import other

app_name = 'other'
urlpatterns = [
    path('trucks/', other.trucks, name='trucks'),
    path('add_truck/', other.add_truck, name='add_truck'),
    path('checkpoints/', other.checkpoints, name='checkpoints'),
    path('add_checkpoint/', other.add_checkpoint, name='add_checkpoint'),
]
