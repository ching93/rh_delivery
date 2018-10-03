from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from the_redhuman_is.models import Worker, Position, Customer
from the_redhuman_is.metro_models import MetroStation
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from html_json_forms import parse_json_form
from django.db.models import Q
from .excel import *
from datetime import date, time, timedelta
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#import time
import re
import json

def main(request):
    return render(request, 'delivery/main.html', {'none': True})

def autocomplete(request):
    q = request.GET.get('q') or ""
    entity = request.GET.get('entity') or None
    if entity == 'driver':
        query = Q(name__icontains=q) if not q == "" else ~Q(name="")
        objects = DeliveryDriver.objects.filter(query)
    elif entity == 'metro':
        query = Q(name__icontains=q) | Q(branch__city__name__icontains=q) if not q == "" else ~Q(name="")
        objects = MetroStation.objects.filter(query)
    else:
        return []
    return [{'id': object.pk, 'text': str(object)} for object in objects]


def all_orders(request):
    day = date.today()
    interval = request.GET.get('interval') or 'day'
    if interval == 'month':
        day = day.replace(day=1)
    elif interval == 'week':
        while day.weekday() != 0:
            day -= timedelta(days=1)
    else:
        day -= timedelta(days=1)
    print(day)
    orders = [order.get_dict() for order in DeliveryOrder.objects.filter(date__gt=day)]
    form_desc = DeliveryOrder.get_form_desc()
    return JsonResponse({'orders': orders,'form_desc': form_desc})

def format_phone(phone):
    clear_phone = "".join([digit if digit in "1234567890" else '' for digit in phone])
    if clear_phone.startswith("8"):
        return "+7"+clear_phone[1:]
    else:
        return "+"+clear_phone

@csrf_exempt
def new_order(request):
    errors = {}
    status = 'error'
    object = None
    if request.GET:
        data = parse_json_form(request.GET)
        print(data)
        entity = data.get('entity', None)
        action = data.get('action', 'create')
        pk = data.get('pk', None)
        form = None
        if entity == 'order':
            if (action == 'edit'):
                instance = DeliveryOrder.objects.filter(pk=pk).first()
                if instance:
                    form = DeliveryOrderForm(data, instance=instance)
            else:
                form = DeliveryOrderForm(data)
        elif entity == 'driver':
            name = data.get("name", None)
            driver = DeliveryDriver.objects.filter(name=name).first()
            if driver:
                phones = data.get('phones', None)
                if phones:
                    phones = [format_phone(phone) for phone in phones]
                    DriverPhone.objects.filter(driver=driver, phone__in=phones).delete()
                    for phone in phones:
                        DriverPhone.objects.create(driver=driver, phone=phone)
                status = 'ok'
            else:
                form = DeliveryDriverForm(data)
        else:
            raise AttributeError
        if form:
            if form.is_valid():
                object = form.save(commit=True)
                if entity == 'order':
                    loader_ids = data.get('new_workers', [])
                    turnouts_new = data.get('turnouts_new', [])
                    DeliveryTurnout.objects.filter(order=object.pk).exclude(pk__in=turnouts_new).delete()
                    status = 'ok'
                    #loader_ids = [str(item) for item in loader_list]#.split(",")
                    errors['turnouts'] = ''
                    for loader in loader_ids:
                        turnoutForm = DeliveryTurnoutForm({'order': pk, 'worker': loader})
                        if turnoutForm.is_valid():
                            turnoutForm.save(commit=True)
                        else:
                            errors['turnouts'] = "Ограничение на добавление грузчика"
                            status = 'error'

                object.refresh_from_db()
                object = object.get_dict()
            else:
                for field in form:
                    errors[field.name] = " ".join(field.errors)
                print(errors)
    print(status)
    print(object)
    return JsonResponse({'status': status, 'errors': errors, 'entity': object})

def update_field(request):
    model_name = request.GET.get('entity')
    field = request.GET.get('field')
    value = request.GET.get('value')
    pk = request.GET.get('pk')
    try:
        if model_name == 'order':
            object = get_object_or_404(DeliveryOrder,pk=pk)
            print(field)
            print(value)
            if field == 'status':
                object.status = value
            if field == 'date':
                object.date = get_date(value)
            if field == 'driver_come_time':
                object.driver_come_time = get_time(value)
            if field == 'driver_postfact_time':
                object.driver_postfact_time = get_time(value)
            if field == 'load_weight':
                object.load_weight = value
            if field == 'load_volume':
                object.load_volume = value
            if field == 'address':
                object.address = value
            if field == 'filial':
                object.filial = value
            if field == 'load_markup':
                object.load_markup = value
            if field == 'loader_number':
                object.loader_number = value
            if field == 'remark':
                object.remark = value
            elif field == 'metro':
                metro = MetroStation.objects.filter(pk=value).first()
                value = {'id': metro.pk, 'text': str(metro)}
                if metro is None:
                    raise Exception('Нет такого метро')
                object.metro = metro
        elif model_name == 'driver':
            object = get_object_or_404(DeliveryDriver,pk=pk)
        object.save()
    except Exception as exc:
        print("error: "+str(exc))
        return JsonResponse({'error': str(exc), 'field': field, 'value': value}, status=400)
    return JsonResponse({'pk': object.pk, 'field': field, 'value': value})

class AjaxResponseMixin:

    def form_invalid(self, form):
        print('invalid')
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        print('valid')
        super(AjaxResponseMixin,self).formn_valid(form)
        return JsonResponse({'pk': self.object.pk})

class DeliveryOrderCreate(AjaxResponseMixin,CreateView):
    model = DeliveryOrder
    fields ='__all__'

class DeliveryOrderUpdate(AjaxResponseMixin,CreateView):
    model = DeliveryOrder
    fields ='__all__'

class DeliveryOrderDelete(AjaxResponseMixin,CreateView):
    model = DeliveryOrder


def read_excel(request):
    customer_id = request.POST.get('customer') or None
    customer = get_object_or_404(Customer, pk=customer_id)
    bytes = request.FILES['excel_file'].read()
    data = read_excel_from_bytes(bytes)
    # Планируемая дата заявки	Груз	Общий вес	Кол-во грузчиков	Объём	Количество мест	Характер груза	Время погрузки/разгрузки	Адрес	Водитель	Номер телефона	Филиал
    headers = data[0]
    headers.append('Ошибка')
    incorrect_rows = []
    saved_rows = 0
    ignored_rows = 0
    inserted_rows = []
    #print(dict(zip(headers,data[1])))
    for row in data[1:]:
        #print(row)
        try:
            last_op = "Неправильная дата"
            print(row[0])
            p_date = row[0]
            load_mark = row[1].strip().rstrip()
            if p_date and DeliveryOrder.objects.filter(date=p_date,load_markup=load_mark,customer=customer).first():
                ignored_rows += 1
                continue
            last_op = "Неправильный формат веса"
            load_weight = float(row[2])
            last_op = "Неправильный формат числа грузчиков"
            loader_num = int(row[3])
            last_op = "Неправильный формат объема груза"
            load_vol = float(row[4])
            last_op = "Неправильный формат времени погрузки/загрузки (ЧЧ:ММ)"
            (first,second) = re.findall("\d{1,2}:\d{1,2}",row[7])
            load_time = get_time(first)
            unload_time = get_time(second)
            last_op = "Адрес отсутствует"
            address = re.sub(" {2,}"," ", row[8].rstrip().lstrip())
            last_op = "Водитель отсутствует"
            driver_name = re.sub(" {2,}"," ", row[9].rstrip().lstrip()).capitalize()
            driver_name = " ".join([name.capitalize() for name in driver_name.split(" ")])
            last_op = "Неправильный формат телефонов"
            driver_phones = [format_phone(phone) for phone in re.findall("\+?[\d\- ]+",str(row[10]))]
            print(driver_phones)
            last_op = "Филиал отсуствует"
            filial = re.sub(" {2,}"," ", row[11].rstrip().lstrip())
            # create drivers
            driver = DeliveryDriver.objects.filter(name=driver_name).first()
            if driver is None:
                driver = DeliveryDriver.objects.create(name=driver_name)
            for phone in driver_phones:
                if DriverPhone.objects.filter(driver=driver,phone=phone).first() is None:
                    DriverPhone.objects.create(driver=driver,phone=phone)
            last_op = "Нельзя создать заявку с такими параметрами"
            order = DeliveryOrder.objects.create(date=p_date, load_markup=load_mark, loader_number=loader_num,
                 load_weight=load_weight, load_volume=load_vol, loading_time=load_time, unloading_time=unload_time,
                 address=address, driver=driver, filial=filial, customer=customer)
            inserted_rows.append(order.get_dict())
        except Exception as e:
            print(str(e))
            print(last_op)
            row.append(last_op + "("+str(e)+")")
            incorrect_rows.append(row)
            continue
    #print(len(inserted_rows))
    return JsonResponse({'status': 'success', 'incorrect_rows': [dict(zip(headers,row)) for row in incorrect_rows],
                         'inserted_rows': inserted_rows, 'saved_rows': saved_rows, 'total_rows': len(data)-1,
                         'ignored_rows': ignored_rows})