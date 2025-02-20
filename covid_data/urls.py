from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CovidDataViewSet

router = DefaultRouter()
router.register(r'covid-data', CovidDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]