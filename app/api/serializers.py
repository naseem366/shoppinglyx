from django.contrib.auth import models
from rest_framework import serializers
from ..models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id','name','locality','city','state','zipcode']
