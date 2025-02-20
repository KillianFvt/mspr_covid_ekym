from rest_framework import viewsets
from .models import CovidData
from .serializers import CovidDataSerializer

class CovidDataViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CovidData instances.

    list:
    Return a list of all the existing CovidData instances.
    URL: GET /api/covid-data/
    Example Response:
    [
        {
            "date": "2023-10-01",
            "country_region": "France",
            "continent": "Europe",
            "population": 67000000,
            "total_cases": 10000000,
            "total_death": 150000,
            "total_recovered": 9500000,
            "active_cases": 350000
        },
        ... more CovidData instances ...
    ]

    retrieve:
    Return the given CovidData instance.
    URL: GET /api/covid-data/{id}/
    Example Response:
    {
        "date": "2023-10-01",
        "country_region": "France",
        "continent": "Europe",
        "population": 67000000,
        "total_cases": 10000000,
        "total_death": 150000,
        "total_recovered": 9500000,
        "active_cases": 350000
    }

    create:
    Create a new CovidData instance.
    URL: POST /api/covid-data/
    Example Request:
    {
        "date": "2023-10-01",
        "country_region": "France",
        "continent": "Europe",
        "population": 67000000,
        "total_cases": 10000000,
        "total_death": 150000,
        "total_recovered": 9500000,
        "active_cases": 350000
    }

    update:
    Update the given CovidData instance.
    URL: PUT /api/covid-data/{id}/
    Example Request:
    {
        "date": "2023-10-01",
        "country_region": "France",
        "continent": "Europe",
        "population": 67000000,
        "total_cases": 10000000,
        "total_death": 150000,
        "total_recovered": 9500000,
        "active_cases": 350000
    }

    partial_update:
    Partially update the given CovidData instance.
    URL: PATCH /api/covid-data/{id}/
    Example Request:
    {
        "total_cases": 10500000
    }

    destroy:
    Delete the given CovidData instance.
    URL: DELETE /api/covid-data/{id}/
    """
    queryset = CovidData.objects.all()
    serializer_class = CovidDataSerializer