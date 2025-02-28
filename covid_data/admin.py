from django.contrib import admin
from .models import CovidData, OWIDCovidData

admin.site.register(CovidData)
admin.site.register(OWIDCovidData)