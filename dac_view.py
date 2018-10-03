from __future__ import unicode_literals

import datetime
from datetime import datetime

from .models import *
from the_redhuman_is.models import Worker, Position

from finance.models import Account as FinanceAccount

from dal import autocomplete
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone


class WorkerDeliveryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print(self.q)
        today = timezone.now()
        if not self.request.user.is_authenticated():
            return Worker.objects.none()
        position = Position.objects.filter(name__istartswith='Грузчик')
        workers = Worker.objects.filter(m_date_of_exp__gt=today,position=position).distinct()
        if self.q:
            workers = workers.filter(
                Q(name__icontains=self.q) |
                Q(last_name__icontains=self.q) |
                Q(patronymic__icontains=self.q) |
                Q(workerpassport__another_passport_number__icontains=self.q)
            ).distinct()
        return workers

class DriverDeliveryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return DeliveryDriver.objects.none()
        drivers = DeliveryDriver.objects.all().distinct()
        if self.q:
            drivers = drivers.filter(
                Q(name__icontains=self.q) |
                Q(phones__phone__icontains=self.q)).distinct()
        return drivers