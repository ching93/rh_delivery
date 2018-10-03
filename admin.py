from django.contrib import admin
from .models import *


admin.site.register(DeliveryOrder)
admin.site.register(DeliveryDriver)
admin.site.register(DeliveryTurnout)
admin.site.register(DriverPhone)