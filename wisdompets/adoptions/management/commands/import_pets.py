import csv
from django.utils import timezone
from django.core.management.base import BaseCommand
from adoptions.models import Pet, Vaccine
from datetime import datetime

class Command(BaseCommand):
    help = 'Import pet data from CSV file'

    def handle(self, *args, **kwargs):
        with open('./pet_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Split the vaccinations by ';' and get or create Vaccine instances
                vaccination_names = row['vaccinations'].split(';')
                vaccines = [Vaccine.objects.get_or_create(name=vac)[0] for vac in vaccination_names]

                # Parse the submission_date as a naive datetime object
                submission_date_naive = datetime.strptime(row['submission_date'], '%Y-%m-%d')

                # Convert the naive datetime to an aware datetime
                submission_date_aware = timezone.make_aware(submission_date_naive, timezone.get_current_timezone())

                pet = Pet.objects.create(
                    name=row['name'],
                    submitter=row['submitter'],
                    species=row['species'],
                    breed=row['breed'],
                    description=row['description'],
                    sex=row['sex'],
                    submission_date=submission_date_aware,
                    age=row['age'],
                )
                # Add the vaccines to the pet
                pet.vaccinations.set(vaccines)
                pet.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported pet data'))
