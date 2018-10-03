from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta, time, date
from the_redhuman_is.models import Worker, Position, Customer
from the_redhuman_is.metro_models import MetroStation
from django.urls import reverse

'''class DeliveryStatusMixin:
    CANCEL = 'Отмена'
    NO_ANSWER = 'Не берет трубку'
    TO_RECALL = 'Перезвонит'
    APPOINTED = 'Назначен'
    NOT_APPOINTED = 'Не назначен'
    ON_PLACE = 'На месте'
    READY = 'Готово'''

ORDER_STATUS = (('NOT_APPOINTED', 'Не назначен'),
                ('APPOINTED', 'Назначен'),
                ('NO_ANSWER', 'Не берет трубку'),
                ('O_RECALL', 'Перезвонит'),
                ('ON_PLACE', 'На месте'),
                ('READY', 'Готово'),
                ('CANCEL', 'Отмена'))

FORMAT_DATE = '%d.%m.%Y'
FORMAT_TIME = '%H:%M'

def get_date_str(datepoint,separator="."):
    return date.strftime(datepoint, FORMAT_DATE.replace(".",separator))

def get_date(str,separator="."):
    return datetime.strptime(str, FORMAT_DATE.replace(".",separator)).date()

def get_time_str(timepoint,separator=":"):
    return time.strftime(timepoint, FORMAT_TIME.replace(":",separator))

def get_time(str,separator=":"):
    return datetime.strptime(str, FORMAT_TIME.replace(":",separator)).time()

class DeliveryDriver(models.Model):
    name = models.TextField(verbose_name="Имя",null=False,blank=False, unique=True)

    def __str__(self):
        return "{} ({})".format(self.name, ",".join([phone.phone for phone in self.phones.all()]))

    def get_dict(self):
        return {'name': self.name, 'phones': [phone.phone for phone in self.phones.all()]}

class DriverPhone(models.Model):
    driver = models.ForeignKey(DeliveryDriver, verbose_name="Водитель",related_name="phones",null=False)
    phone = models.TextField(verbose_name="Телефон", null=False,blank=False,max_length=12)

    def __str__(self):
        return self.phone


class DeliveryOrder(models.Model):
    date = models.DateField(default=now, null=False, verbose_name='Планируемая дата и время')
    loading_time = models.TimeField(default=now, null=False, verbose_name='Время с')
    unloading_time = models.TimeField(default=now, null=False, verbose_name='Время по')
    driver_come_time = models.TimeField(default=None, null=True, blank=True, verbose_name='Время прихода водителя')
    driver_postfact_time = models.TimeField(default=None, null=True, blank=True, verbose_name='Фактическое время прихода водителя')
    address = models.TextField(null=False, verbose_name="Адрес")
    metro = models.ForeignKey(MetroStation, null=True,blank=True)
    filial = models.TextField(null=False)
    load_markup = models.TextField(verbose_name="Маркировка груза")
    load_weight = models.FloatField(verbose_name="Вес груза",null=True)
    load_volume = models.FloatField(verbose_name="Объем груза",null=True)
    driver = models.ForeignKey(DeliveryDriver, verbose_name="Водитель",null=True,blank=True)
    customer = models.ForeignKey(Customer, verbose_name="Клиент",null=True)
    loader_number = models.IntegerField(default=1, verbose_name="Желаемое число грузчиков")
    remark = models.TextField(blank=True, verbose_name="Примечание")
    status = models.TextField(verbose_name="Статус",choices=ORDER_STATUS, default=ORDER_STATUS[0][0])

    def get_dict(self):
        result = {}
        result['pk'] = self.pk
        result['date'] = get_date_str(self.date)
        result['loading_time'] = get_time_str(self.loading_time)
        result['unloading_time'] = get_time_str(self.unloading_time)
        result['driver_come_time'] = get_time_str(self.driver_come_time) if self.driver_come_time else None
        result['driver_postfact_time'] = get_time_str(self.driver_postfact_time) if self.driver_postfact_time else None
        result['driver'] = { 'pk': self.driver.pk, 'text': str(self.driver)} if self.driver else None
        result['load_weight'] = self.load_weight
        result['load_volume'] = self.load_volume
        result['metro'] = { 'pk': self.metro.pk, 'text': str(self.metro)} if self.metro else None
        result['address'] = self.address
        result['filial'] = self.filial
        result['load_markup'] = self.load_markup
        result['turnouts'] = [turnout.get_dict() for turnout in self.turnouts.all()]
        result['loader_number'] = self.loader_number
        result['remark'] = self.remark
        result['customer'] = { 'pk': self.customer.pk, 'text': str(self.customer)}
        result['status'] = self.status

        return result

    @staticmethod
    def get_form_desc():
        form = {}
        now = datetime.now()
        labels = {'date': 'Дата', 'loading_time': 'Время с', 'unloading_time': 'Время по', 'address': 'Адрес', 'filial': 'Филиал',
                  'load_markup': 'Маркировка', 'load_weight': 'Вес', 'load_volume': 'Объем',
                  'driver': 'Водитель','customer': 'Клиент','loader_number': 'Число грузчиков',
                  'metro': 'Метро', 'status': 'Статус','turnouts': 'Грузчики','remark': 'Примечание',
                  'driver_come_time': 'Время прихода водителя', 'driver_postfact_time': 'Фактическое время прихода водителя' }
        types = {'date': 'text', 'loading_time': 'text', 'unloading_time': 'text', 'address': 'text', 'filial': 'text',
                  'load_markup': 'text', 'load_weight': 'float', 'load_volume': 'float', 'driver': 'select', 'loader_number': 'number', 'customer': 'select',
                  'metro': 'select', 'status': 'choice','turnouts': 'select-multiple','remark': 'textarea',
                 'driver_come_time': 'text', 'driver_postfact_time': 'text'}
        defaults = {'date': get_date_str(now.date()), 'loading_time': get_time_str(now.time()),'unloading_time': get_time_str(now.time()),
            'address': 'г.М', 'filial': 'Главный', 'loader_number': 1,  'status': ORDER_STATUS[0][0]}
        required = {'date': True, 'loading_time': True, 'unloading_time': True, 'address': True, 'filial': True,
                  'load_markup': True, 'load_weight': True, 'load_volume': True, 'driver': True, 'loader_number': True, 'customer': True,
                  'metro': False, 'status': False,'turnouts': False,'remark': False,
                    'driver_come_time': False, 'driver_postfact_time': False}
        urls = {'driver': reverse('delivery:driver-autocomplete'), 'customer': reverse('the_redhuman_is:customer-autocomplete'),
                'turnouts': reverse('delivery:worker-autocomplete'), 'metro': reverse("the_redhuman_is:metro-station-autocomplete")}
        choices = {'status': {choice[0]: choice[1] for choice in ORDER_STATUS} }
        form['labels'] = labels
        form['types'] = types
        form['urls'] = urls
        form['defaults'] = defaults
        form['choices'] = choices
        form['required'] = required
        return form

    def __str__(self):
        return "{} {} {}".format(self.customer, self.driver, self.filial)


class DeliveryTimesheet(models.Model):
    order = models.OneToOneField(DeliveryOrder,verbose_name='Заказ',related_name='timesheet')
    timepoint = models.DateTimeField(default=now, null=False, verbose_name="Время доставки")

    def __str__(self):
        return "{} {}".format(self.name, self.phone)

    def get_dict(self):
        return {'order': self.order, 'timepoint': self.timepoint}

class DeliveryTurnout(models.Model):
    order = models.ForeignKey(DeliveryOrder,verbose_name='Заказ',related_name='turnouts')
    worker = models.ForeignKey(Worker,null=False,verbose_name='Грузчик')
    #timepoint = models.DateTimeField(default=now, null=False, verbose_name="Время выхода")


    def save(self,*args, **kwargs):
        if not self.worker.position.name.startswith("Грузчик"):
            raise AttributeError
        if (self.order.turnouts.count() == self.order.loader_number):
            self.order.status = ORDER_STATUS[1][0]

        super().save(*args, **kwargs)

    def get_dict(self):
        return {'pk': self.pk, 'order': self.order.pk, 'text': str(self.worker), 'worker_id': self.worker.pk}

