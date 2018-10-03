from django.conf.urls import url
from . import views
from . import dac_view

app_name = 'delivery'

urlpatterns = [
    url(r'^$', views.main, name='order'),
    url(r'^all/$', views.all_orders, name='orders'),
    url(r'^new', views.new_order, name='new'),
    url(r'^update', views.update_field, name='update'),
    url(r'^worker-autocomplete', dac_view.WorkerDeliveryAutocomplete.as_view(), name='worker-autocomplete'),
    url(r'^driver-autocomplete', dac_view.DriverDeliveryAutocomplete.as_view(), name='driver-autocomplete'),
    #url(r"^autocomplete",views.autocomplete, name="autocomplete")
    url(r"^parse_excel", views.read_excel, name="parse-excel"),
    #url(r"order/(?P<pk>\d+)/update/$", views.DeliveryOrderUpdate.as_view(), name='order-update'),
    #url(r"order/(?P<pk>\d+)/delete/$", views.DeliveryOrderDelete.as_view(), name='order-delete'),
    #url(r"order/(?P<pk>\d+)/create/$", views.DeliveryOrderCreate.as_view(), name='order-create')
]