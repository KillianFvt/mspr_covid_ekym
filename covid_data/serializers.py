from rest_framework import serializers
from .models import CovidData

class CovidDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidData
        fields = '__all__'