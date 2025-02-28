from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, BigIntegerField
from .models import CovidData, OWIDCovidData
from .serializers import CovidDataSerializer, OWIDCovidDataSerializer

class CovidDataViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CovidData instances.

    [Documentation existante maintenue]
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
            active_cases=sum([country.active_cases for country in all_countries if country.active_cases is not None])
        )

        top_countries = list(top_countries)
        top_countries.append(rest_country)

        serializer = CovidDataSerializer(top_countries, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='averages')
    def get_averages(self, request):
        """
        Return the averages of total cases, total deaths, total recovered, and active cases.
        URL: GET /api/covid-data/averages/
        """

        total_population = CovidData.objects.aggregate(total_population=Sum('population'))['total_population']

        return Response({
            "total_pop": total_population,
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
    """
    queryset = OWIDCovidData.objects.all()
    serializer_class = OWIDCovidDataSerializer

    @action(detail=False, methods=['GET'], url_path='top-locations')
    def get_top_locations(self, request):
        """
        Return the top n locations with the highest number of total cases.
        URL: GET /api/owid-covid-data/top-locations/?top=n
        """
        location_amt = int(request.query_params.get('top', 24))

        # Groupe par location et prend la dernière date pour chaque location
        latest_data = {}
        for data in OWIDCovidData.objects.all():
            location = data.location
            if location not in latest_data or data.date > latest_data[location].date:
                latest_data[location] = data

        # Convertit le dictionnaire en liste et trie par total_cases
        sorted_locations = sorted(
            latest_data.values(),
            key=lambda x: x.total_cases if x.total_cases is not None else 0,
            reverse=True
        )

        top_locations = sorted_locations[:location_amt]
        other_locations = sorted_locations[location_amt:]

        serializer = OWIDCovidDataSerializer(top_locations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='statistics')
    def get_statistics(self, request):
        """
        Return global statistics from the OWID data.
        URL: GET /api/owid-covid-data/statistics/
        """
        # Groupe par location et prend la dernière date pour chaque location
        latest_data = {}
        for data in OWIDCovidData.objects.all():
            location = data.location
            if location not in latest_data or data.date > latest_data[location].date:
                latest_data[location] = data

        total_cases = sum(data.total_cases for data in latest_data.values() if data.total_cases is not None)
        total_deaths = sum(data.total_deaths for data in latest_data.values() if data.total_deaths is not None)
        total_population = sum(data.population for data in latest_data.values() if data.population is not None)

        return Response({
            "total_cases": total_cases,
            "total_deaths": total_deaths,
            "total_population": total_population,
            "case_fatality_rate": total_deaths / total_cases if total_cases else 0,
            "cases_per_million": (total_cases * 1000000) / total_population if total_population else 0,
            "deaths_per_million": (total_deaths * 1000000) / total_population if total_population else 0
        })