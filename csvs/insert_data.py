import csv
import json
import os
import traceback

import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mspr_covid_ekym.settings')
django.setup()

from covid_data.models import CovidData

csv_file_path = r'worldometer_data.csv'

def insert_data_from_csv(file_path):
    covid_data_list = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                covid_data = CovidData(
                    country_region=row['Country/Region'],
                    continent=row['Continent'],
                    population=int(row['Population'] if row['Population'] else 0),
                    total_cases=int(row['TotalCases']) if row['TotalCases'] else 0,
                    total_deaths=int(row['TotalDeaths']) if row['TotalDeaths'] else 0,
                    total_recovered=int(row['TotalRecovered']) if row['TotalRecovered'] else 0,
                    active_cases=int(row['ActiveCases']) if row['ActiveCases'] else 0
                )
                covid_data_list.append(covid_data)
    except Exception as e:
        print(f'Error: {e}')
        print(traceback.format_exc())
    else:
        # print([covid_data.to_dict() for covid_data in covid_data_list])
        CovidData.objects.bulk_create(covid_data_list)


if __name__ == '__main__':
    insert_data_from_csv(csv_file_path)