from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, BigIntegerField
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

    @action(detail=False, methods=['GET'], url_path='top-countries')
    def get_top_countries(self, request):
        """
        Return the top n countries with the highest number of total cases.
        URL: GET /api/covid-data/top-countries/?top=n
        """
        country_amt = int(request.query_params.get('top', 24))

        top_countries = CovidData.objects.order_by('-population')[:country_amt + 1]

        all_countries = CovidData.objects.order_by('-population')[country_amt + 1:]
        rest_country = CovidData(
            country_region='Other',
            continent='Other',
            population=sum([country.population for country in all_countries if country.population is not None]),
            total_cases=sum([country.total_cases for country in all_countries if country.total_cases is not None]),
            total_deaths=sum([country.total_deaths for country in all_countries if country.total_deaths is not None]),
            total_recovered=sum([country.total_recovered for country in all_countries if country.total_recovered is not None]),
        )

        top_countries = list(top_countries)
        top_countries.append(rest_country)

        serializer = CovidDataSerializer(top_countries, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='world-ratios')
    def get_world_ratios(self, request):
        """
        Return the ratio of total cases, total deaths, total recovered, and active cases.
        URL: GET /api/covid-data/world-ratios/
        """

        total_population = CovidData.objects.filter(population__isnull=False).aggregate(Sum('population'))['population__sum']

        total_cases = CovidData.objects.filter(total_cases__isnull=False).aggregate(Sum('total_cases'))['total_cases__sum']
        total_deaths = CovidData.objects.filter(total_deaths__isnull=False).aggregate(Sum('total_deaths'))['total_deaths__sum']
        total_recovered = CovidData.objects.filter(total_recovered__isnull=False).aggregate(Sum('total_recovered'))['total_recovered__sum']

        return Response({
            'ratio_cases': total_cases / total_population * 100,
            'ratio_deaths': total_deaths / total_cases * 100,
            'ratio_recovered': total_recovered / total_cases * 100,
        })