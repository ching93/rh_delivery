from .models import DeliveryOrder, DeliveryTurnout, DeliveryDriver, DriverPhone
from the_redhuman_is.models import Worker, Position
from rest_framework import serializers

class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = "__all__"


class DriverPhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverPhone
        fields = "__all__"

class DriverSerializer(serializers.ModelSerializer):


    class Meta:
        model = DeliveryDriver
        fields = "__all__"

class DeliveryTurnoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryTurnout
        fields = "__all__"

class DeliveryOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryOrder
        fields = "__all__"