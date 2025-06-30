from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class CovidDataApiTest(APITestCase):
    def setUp(self):
        self.covid_data = {
            "country_region": "France",
            "continent": "Europe",
            "population": 67000000,
            "total_cases": 1000000,
            "total_deaths": 20000,
            "total_recovered": 900000
        }
        self.owid_data = {
            "iso_code": "FR",
            "continent": "Europe",
            "location": "France",
            "date": "2023-01-01",
            "total_cases": 1000000,
            "new_cases": 1000,
            "total_deaths": 20000,
            "new_deaths": 10,
            "total_cases_per_million": 15000,
            "new_cases_per_million": 15,
            "total_deaths_per_million": 300,
            "new_deaths_per_million": 0.2,
            "population_density": 120,
            "median_age": 42,
            "aged_65_older": 20,
            "aged_70_older": 10,
            "gdp_per_capita": 40000,
            "cardiovasc_death_rate": 100,
            "diabetes_prevalence": 5,
            "life_expectancy": 82,
            "population": 67000000
        }

    def test_list_covid_data(self):
        url = "/api/covid-data/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())

    def test_create_covid_data(self):
        url = "/api/covid-data/"
        response = self.client.post(url, self.covid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["country_region"], "France")

    def test_retrieve_covid_data(self):
        # Création d'une instance pour test
        post = self.client.post("/api/covid-data/", self.covid_data, format="json")
        covid_id = post.data["id"]
        url = f"/api/covid-data/{covid_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["country_region"], "France")

    def test_update_covid_data(self):
        post = self.client.post("/api/covid-data/", self.covid_data, format="json")
        covid_id = post.data["id"]
        url = f"/api/covid-data/{covid_id}/"
        update = self.covid_data.copy()
        update["total_cases"] = 2000000
        response = self.client.put(url, update, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_cases"], 2000000)

    def test_delete_covid_data(self):
        post = self.client.post("/api/covid-data/", self.covid_data, format="json")
        covid_id = post.data["id"]
        url = f"/api/covid-data/{covid_id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_owid_covid_data(self):
        url = "/api/owid-covid-data/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())

    def test_create_owid_covid_data(self):
        url = "/api/owid-covid-data/"
        response = self.client.post(url, self.owid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["iso_code"], "FR")

    def test_retrieve_owid_covid_data(self):
        post = self.client.post("/api/owid-covid-data/", self.owid_data, format="json")
        owid_id = post.data["id"]
        url = f"/api/owid-covid-data/{owid_id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["iso_code"], "FR")