from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CovidDataViewSet, OWIDCovidDataViewSet

router = DefaultRouter()
router.register(r'covid-data', CovidDataViewSet)
router.register(r'owid-covid-data', OWIDCovidDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]