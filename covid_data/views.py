from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import CovidData, OWIDCovidData
from .serializers import CovidDataSerializer, OWIDCovidDataSerializer


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

        top_countries = CovidData.objects.order_by('-population')[:country_amt]

        all_countries = CovidData.objects.order_by('-population')[country_amt:]
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
        Country instances with missing data will be excluded from the calculation.
        URL: GET /api/covid-data/world-ratios/
        """

        valid_covid_data = CovidData.objects.filter(
            population__isnull=False,
            total_cases__isnull=False,
            total_deaths__isnull=False,
            total_recovered__isnull=False,
        )

        total_population = valid_covid_data.aggregate(Sum('population'))['population__sum']

        total_cases = valid_covid_data.aggregate(Sum('total_cases'))['total_cases__sum']
        total_deaths = valid_covid_data.aggregate(Sum('total_deaths'))['total_deaths__sum']
        total_recovered = valid_covid_data.aggregate(Sum('total_recovered'))['total_recovered__sum']

        return Response({
            'ratio_cases': total_cases / total_population * 100,
            'ratio_deaths': total_deaths / total_cases * 100,
            'ratio_recovered': total_recovered / total_cases * 100,
        })


class OWIDCovidDataViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing OWIDCovidData instances.

    list:
    Return a list of all the existing OWIDCovidData instances.
    URL: GET /api/owid-covid-data/

    retrieve:
    Return the given OWIDCovidData instance.
    URL: GET /api/owid-covid-data/{id}/

    create:
    Create a new OWIDCovidData instance.
    URL: POST /api/owid-covid-data/

    update:
    Update the given OWIDCovidData instance.
    URL: PUT /api/owid-covid-data/{id}/

    partial_update:
    Partially update the given OWIDCovidData instance.
    URL: PATCH /api/owid-covid-data/{id}/

    destroy:
    Delete the given OWIDCovidData instance.
    URL: DELETE /api/owid-covid-data/{id}/

    Filters available:
    - location : /api/owid-covid-data/?location=France
    - date : /api/owid-covid-data/?date=2023-10-01
    - iso_code : /api/owid-covid-data/?iso_code=FRA

    Page limit available:
    - limit : /api/owid-covid-data/?limit=50 (amount of items per page)
    - offset : /api/owid-covid-data/?offset=50 (starting point for the next page)
    """

    queryset = OWIDCovidData.objects.all()
    serializer_class = OWIDCovidDataSerializer
    filterset_fields = ['location', 'date']
    ordering_fields = ['location', 'date']
    ordering = ['date']
    search_fields = ['location', 'iso_code']
    filter_backends = [DjangoFilterBackend]