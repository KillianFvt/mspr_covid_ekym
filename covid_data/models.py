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


class OWIDCovidData(models.Model):
    iso_code = models.CharField(max_length=10)
    continent = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100)
    date = models.DateField()
    total_cases = models.FloatField(null=True, blank=True)
    new_cases = models.FloatField(null=True, blank=True)
    total_deaths = models.FloatField(null=True, blank=True)
    new_deaths = models.FloatField(null=True, blank=True)
    total_cases_per_million = models.FloatField(null=True, blank=True)
    new_cases_per_million = models.FloatField(null=True, blank=True)
    total_deaths_per_million = models.FloatField(null=True, blank=True)
    new_deaths_per_million = models.FloatField(null=True, blank=True)
    population_density = models.FloatField(null=True, blank=True)
    median_age = models.FloatField(null=True, blank=True)
    aged_65_older = models.FloatField(null=True, blank=True)
    aged_70_older = models.FloatField(null=True, blank=True)
    gdp_per_capita = models.FloatField(null=True, blank=True)
    cardiovasc_death_rate = models.FloatField(null=True, blank=True)
    diabetes_prevalence = models.FloatField(null=True, blank=True)
    life_expectancy = models.FloatField(null=True, blank=True)
    population = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ['location', 'date']
        indexes = [
            models.Index(fields=['location']),
            models.Index(fields=['date']),
            models.Index(fields=['iso_code']),
        ]

    def __str__(self):
        return f"{self.location} - {self.date}"

    def to_dict(self):
        return {
            'iso_code': self.iso_code,
            'continent': self.continent,
            'location': self.location,
            'date': self.date,
            'total_cases': self.total_cases,
            'new_cases': self.new_cases,
            'total_deaths': self.total_deaths,
            'new_deaths': self.new_deaths,
            'total_cases_per_million': self.total_cases_per_million,
            'new_cases_per_million': self.new_cases_per_million,
            'total_deaths_per_million': self.total_deaths_per_million,
            'new_deaths_per_million': self.new_deaths_per_million,
            'population_density': self.population_density,
            'median_age': self.median_age,
            'aged_65_older': self.aged_65_older,
            'aged_70_older': self.aged_70_older,
            'gdp_per_capita': self.gdp_per_capita,
            'cardiovasc_death_rate': self.cardiovasc_death_rate,
            'diabetes_prevalence': self.diabetes_prevalence,
            'life_expectancy': self.life_expectancy,
            'population': self.population
        }