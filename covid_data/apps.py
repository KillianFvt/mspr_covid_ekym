from django.apps import AppConfig


class CovidDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'covid_data'

class OWIDCovidDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'owidcovid_data'