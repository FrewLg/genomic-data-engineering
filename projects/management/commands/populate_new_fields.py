# management/commands/populate_new_fields.py
from django.core.management.base import BaseCommand
from yourapp.models import SamplesMetadata
import csv

class Command(BaseCommand):
    help = "Populate new sample fields from CSV"

    def handle(self, *args, **options):
        with open('populate.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    s = SamplesMetadata.objects.get(sample_id=row['sample_id'])
                    s.serotype = row.get('serotype') or s.serotype
                    # set other fields...
                    s.save()
                except SamplesMetadata.DoesNotExist:
                    self.stdout.write(f"Missing sample {row['sample_id']}")
