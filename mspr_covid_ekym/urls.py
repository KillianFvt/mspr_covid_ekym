from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('covid_data.urls')),
    path(
        "openapi",
        get_schema_view(
            title="MSPR Covid Data",
            description="A project for an MSPR made by Egor, Killian, Martin, Youssef",
            version="1.0.0"
        ),
        name="openapi-schema",
    ),
]