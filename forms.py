from django import forms
from .models import *
from the_redhuman_is.metro_models import MetroStation

class DeliveryOrderForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%d.%m.%Y',])
    loading_time = forms.TimeField(input_formats=['%H:%M',])
    unloading_time = forms.TimeField(input_formats=['%H:%M',])
    driver_come_time = forms.TimeField(input_formats=['%H:%M',],required=False)
    driver_postfact_time = forms.TimeField(input_formats=['%H:%M',],required=False)

    class Meta:
        model = DeliveryOrder
        fields = "__all__"

class DeliveryDriverForm(forms.ModelForm):

    class Meta:
        model = DeliveryDriver
        fields = ('name',)


class DeliveryTurnoutForm(forms.ModelForm):

    class Meta:
        model = DeliveryTurnout
        fields = ('order', 'worker')

class ExcelUploadForm(forms.Form):
    file = forms.FileField()