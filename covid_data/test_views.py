from rest_framework.test import APITestCase
from rest_framework import status
from .models import CovidData

class CovidDataCustomViewsTest(APITestCase):
    def setUp(self):
        # Création de plusieurs pays pour les tests
        CovidData.objects.create(
            country_region="France", continent="Europe", population=67000000,
            total_cases=10000000, total_deaths=150000, total_recovered=9500000
        )
        CovidData.objects.create(
            country_region="Allemagne", continent="Europe", population=83000000,
            total_cases=9000000, total_deaths=120000, total_recovered=8500000
        )
        CovidData.objects.create(
            country_region="Italie", continent="Europe", population=60000000,
            total_cases=8000000, total_deaths=130000, total_recovered=7500000
        )
        CovidData.objects.create(
            country_region="Espagne", continent="Europe", population=47000000,
            total_cases=7000000, total_deaths=110000, total_recovered=6500000
        )

    def test_get_top_countries_default(self):
        url = "/api/covid-data/top-countries/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Par défaut, top=24 donc tous les pays + "Other"
        self.assertGreaterEqual(len(response.data), 4)
        # Le dernier doit être "Other"
        self.assertEqual(response.data[-1]['country_region'], 'Other')

    def test_get_top_countries_with_param(self):
        url = "/api/covid-data/top-countries/?top=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 2 pays + "Other"
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[-1]['country_region'], 'Other')

    def test_get_world_ratios(self):
        url = "/api/covid-data/world-ratios/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Vérifie la présence des ratios attendus
        self.assertIn('ratio_cases', response.data)
        self.assertIn('ratio_deaths', response.data)
        self.assertIn('ratio_recovered', response.data)
        # Les ratios doivent être des nombres
        self.assertIsInstance(response.data['ratio_cases'], float)
        self.assertIsInstance(response.data['ratio_deaths'], float)
        self.assertIsInstance(response.data['ratio_recovered'], float)