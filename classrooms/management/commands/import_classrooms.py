import json, pathlib
from django.core.management.base import BaseCommand
from classrooms.services import upsert_classroom_payload
from django.db import transaction

class Command(BaseCommand):
    help = "Import classrooms JSON (idempotent upsert)"

    def add_arguments(self, parser):
        parser.add_argument("--path", required=True)
        
    def handle(self, *args, **opts):
        data = json.loads(pathlib.Path(opts["path"]).read_text())
        n = 0
        with transaction.atomic():
            for item in data.get("classrooms", []):
                upsert_classroom_payload(item)
                n += 1
        self.stdout.write(self.style.SUCCESS(f"Upserted {n} classrooms"))
