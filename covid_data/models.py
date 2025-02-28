from django.db import models

class CovidData(models.Model):
    country_region = models.CharField(max_length=100)
    continent = models.CharField(max_length=100)
    population = models.IntegerField(null=True)
    total_cases = models.IntegerField(null=True)
    total_deaths = models.IntegerField(null=True)
    total_recovered = models.IntegerField(null=True)
    active_cases = models.IntegerField(null=True)

    def __str__(self):
        return self.country_region

    def to_dict(self):
        return {
            'country_region': self.country_region,
            'continent': self.continent,
            'population': self.population,
            'total_cases': self.total_cases,
            'total_death': self.total_deaths,
            'total_recovered': self.total_recovered,
            'active_cases': self.active_cases
        }