from django.db import models

class CovidData(models.Model):
    date = models.DateField()
    country_region = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    population = models.IntegerField()
    total_cases = models.IntegerField()
    total_death = models.IntegerField()
    total_recovered = models.IntegerField()
    active_cases = models.IntegerField()

    def __str__(self):
        return self.country_region