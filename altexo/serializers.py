import djoser.serializers
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Invoice, Subscription, Service


class CustomUserRegistrationSerializer(djoser.serializers.UserRegistrationSerializer):
    """
    User registration serializer which checks if a email from a request is unique.
    """
    def validate_email(self, value):
        if User.objects.filter(email=value): #.exclude(username=username).count():
            raise serializers.ValidationError(u'This field must be unique.')
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    """
    Invoice serializer
    """    
    class Meta:
        model = Invoice
        fields = [
            'id', 
            'dt_created', 
            'dt_modified', 
            'user', 
            'status', 
            'amount',
        ]
        ordering = ['-dt_created']


class ServiceSerializer(serializers.ModelSerializer):
    """
    Service serializer
    """    
    class Meta:
        model = Service
        fields = [
            'id', 
            'name', 
            'price',
        ]
        ordering = ['name']


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Subscription serializer
    """    
    class Meta:
        model = Subscription
        fields = [
            'id', 
            'dt_created', 
            'dt_renewed', 
            'user', 
            'service', 
        ]
        ordering = ['-dt_created']