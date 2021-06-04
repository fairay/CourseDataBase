from django.urls import path
from main.views import other
from logger import view_log

app_name = 'other'
urlpatterns = [
    path('trucks/', view_log(other.trucks), name='trucks'),
    path('add_truck/', view_log(other.add_truck), name='add_truck'),

    path('checkpoints/', view_log(other.checkpoints), name='checkpoints'),
    path('add_checkpoint/', view_log(other.add_checkpoint), name='add_checkpoint'),

    path('delivery/', view_log(other.delivery), name='delivery'),
    path('delivery/<int:orderid>', view_log(other.delivery_page), name='delivery_page'),
    path('delivery/assign/', view_log(other.assign_delivery), name='assign_delivery'),
    path('delivery/pick/<int:orderid>', view_log(other.pick_delivey), name='pick_delivery'),
    path('delivery/done/<int:orderid>', view_log(other.done_delivery), name='done_delivery'),
    path('add_delivery/', view_log(other.add_delivery), name='add_delivery'),

    path('pass_record/', view_log(other.pass_record), name='pass_record'),
    path('pass_record/my', view_log(other.driver_pass_record), name='driver_pass_record'),
    path('pass_record/guard', view_log(other.guard_pass_record), name='guard_pass_record'),
    path('pass_record/add', view_log(other.add_pass_record), name='add_pass_record'),
]
