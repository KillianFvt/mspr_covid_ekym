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
                    date=datetime.now().date(),  # Assuming the date is the current date
                    country_region=row['Country/Region'],
                    continent=row['Continent'],
                    population=int(row['Population']),
                    total_cases=int(row['TotalCases']),
                    total_death=int(row['TotalDeaths']),
                    total_recovered=int(row['TotalRecovered']),
                    active_cases=int(row['ActiveCases'])
                )
                covid_data_list.append(covid_data)
    except Exception as e:
        print(f'Error: {e}')
        print(traceback.format_exc())
    else:
        # print([covid_data.to_dict() for covid_data in covid_data_list])
        CovidData.objects.bulk_create(covid_data_list)

insert_data_from_csv(csv_file_path)