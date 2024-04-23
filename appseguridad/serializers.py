from rest_framework  import serializers
from appevaluacion.models import *
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
