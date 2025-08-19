from django.db import transaction
from .models import Classroom, Panorama

@transaction.atomic
def upsert_classroom_payload(c: dict):
        # validate minimal required keys
    assert "external_id" in c and "building" in c and "room_number" in c
    cls, _ = Classroom.objects.update_or_create(
        external_id=c["external_id"],
        defaults={
            "building": c.get("building",""),
            "room_number": c.get("room_number",""),
            "capacity": c.get("capacity",0),
            "summary": c.get("summary",""),
            "is_published": c.get("is_published", True),
            "attributes": c.get("attributes", {}), 

        },
    )
    for p in sorted(c.get("panoramas", []), key=lambda x: x.get("order", 0)):
        Panorama.objects.update_or_create(
            external_id=p["external_id"],
            defaults={
                "classroom": cls,
                "name": p.get("name",""),
                "image_url": p["image_url"],
                "preview_url": p.get("preview_url",""),
                "yaw": p.get("yaw", 0),
                "pitch": p.get("pitch", 0),
                "hfov": p.get("hfov", 90),
                "order": p.get("order", 0),
            },
        )
