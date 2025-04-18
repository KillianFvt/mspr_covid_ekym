import csv
import os
import django
from datetime import datetime

from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mspr_covid_ekym.settings')
django.setup()

from covid_data.models import OWIDCovidData

def import_from_csv(file_path):
    batch_size = 10000  # Batch size for insertion
    objects = []  # List to store objects for bulk insertion
    count = 0
    count_new = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            def parse_value(value):
                return None if value == '' or value.lower() == 'null' else value

            def safe_float(value):
                try:
                    return float(value) if parse_value(value) is not None else None
                except (ValueError, TypeError):
                    return None

            def safe_int(value):
                try:
                    val = safe_float(value)
                    return int(val) if val is not None else None
                except (ValueError, TypeError):
                    return None

            date_str = row['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Create an OWIDCovidData object
            obj = OWIDCovidData(
                location=parse_value(row.get('location')),
                date=date_obj,
                iso_code=parse_value(row.get('iso_code')),
                continent=parse_value(row.get('continent')),
                total_cases=safe_float(row.get('total_cases')),
                new_cases=safe_float(row.get('new_cases')),
                total_deaths=safe_float(row.get('total_deaths')),
                new_deaths=safe_float(row.get('new_deaths')),
                total_cases_per_million=safe_float(row.get('total_cases_per_million')),
                new_cases_per_million=safe_float(row.get('new_cases_per_million')),
                total_deaths_per_million=safe_float(row.get('total_deaths_per_million')),
                new_deaths_per_million=safe_float(row.get('new_deaths_per_million')),
                population_density=safe_float(row.get('population_density')),
                median_age=safe_float(row.get('median_age')),
                aged_65_older=safe_float(row.get('aged_65_older')),
                aged_70_older=safe_float(row.get('aged_70_older')),
                gdp_per_capita=safe_float(row.get('gdp_per_capita')),
                cardiovasc_death_rate=safe_float(row.get('cardiovasc_death_rate')),
                diabetes_prevalence=safe_float(row.get('diabetes_prevalence')),
                life_expectancy=safe_float(row.get('life_expectancy')),
                population=safe_int(row.get('population'))
            )
            objects.append(obj)
            count += 1

            # Insert in batches when batch size is reached
            if len(objects) >= batch_size:
                try:
                    OWIDCovidData.objects.bulk_create(objects)
                    count_new += len(objects)
                except django.db.utils.IntegrityError as e:
                    print(f"IntegrityError encountered: {e}. Attempting to insert rows individually.")
                    for obj in objects:
                        try:
                            obj.save()
                            count_new += 1
                        except django.db.utils.IntegrityError:
                            print(f"Skipping row with unique constraint violation: {obj}")
                objects = []  # Reset the list
                print(f"{count} records processed, {count_new} new...")

        # Insert remaining objects
        if objects:
            try:
                OWIDCovidData.objects.bulk_create(objects)
                count_new += len(objects)
            except django.db.utils.IntegrityError as e:
                print(f"IntegrityError encountered: {e}. Attempting to insert rows individually.")
                for obj in objects:
                    try:
                        obj.save()
                        count_new += 1
                    except django.db.utils.IntegrityError:
                        print(f"Skipping row with unique constraint violation: {obj}")

    print(f"Import completed. {count} records processed, {count_new} new.")

if __name__ == "__main__":
    import_from_csv("owid-covid-data_cleaned.csv")