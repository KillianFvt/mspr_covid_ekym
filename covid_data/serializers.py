from rest_framework import serializers
from .models import CovidData, OWIDCovidData

class CovidDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CovidData
        fields = '__all__'

class OWIDCovidDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OWIDCovidData
        fields = '__all__'