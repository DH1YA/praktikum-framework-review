from rest_framework import serializers
from .models import Students
class StudentsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Students
    fields = ['id', 'nim', 'name', 'email', 'phone_number', 'year',
    'teacher'] # Field yang ingin kamu expose di API