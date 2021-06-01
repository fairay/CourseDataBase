from django.urls import path
from main.views import other

app_name = 'other'
urlpatterns = [
    path('trucks/', other.trucks, name='trucks'),
    path('add_truck/', other.add_truck, name='add_truck'),
    path('checkpoints/', other.checkpoints, name='checkpoints'),
    path('add_checkpoint/', other.add_checkpoint, name='add_checkpoint'),
    path('delivery/', other.delivery, name='delivery'),
    path('delivery/<int:orderid>', other.delivery_page, name='delivery_page'),
    path('delivery/assign/', other.assign_delivery, name='assign_delivery'),
    path('delivery/done/<int:orderid>', other.done_delivery, name='done_delivery'),
    path('add_delivery/', other.add_delivery, name='add_delivery'),
    path('pass_record/', other.pass_record, name='pass_record'),
    path('pass_record/add', other.add_pass_record, name='add_pass_record'),
]
