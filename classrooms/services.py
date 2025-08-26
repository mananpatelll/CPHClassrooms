from django.db import transaction
from .models import Building, Classroom, Panorama

def _yn(v):
    if isinstance(v, bool): return v
    return str(v).strip().lower() in {"yes","true","1"}

@transaction.atomic
def upsert_classroom_payload(c: dict):
    # 1) building
    bname = c.get("building","").strip()
    building, _ = Building.objects.get_or_create(name=bname)

    # 2) classroom
    attrs = c.get("attributes", {}) or {}
    cls, _ = Classroom.objects.update_or_create(
        external_id=c["external_id"],
        defaults={
            "building": building,
            "room_number": c.get("room_number",""),
            "capacity": c.get("capacity",0),
            "summary": c.get("summary",""),
            "is_published": c.get("is_published", True),
            "preview_image": c.get("preview_image", ""),

            "voice_amplification": _yn(attrs.get("Voice Amplification")),
            "class_capture": _yn(attrs.get("Class Capture")),
            "web_conference": _yn(attrs.get("Web Conference")),
            "handheld_microphone": _yn(attrs.get("Handheld Microphone")),
            "document_camera": _yn(attrs.get("Document Camera")),
            "ceiling_microphone": _yn(attrs.get("Web Conference Microphone")) or _yn(attrs.get("Ceiling-mounted microphone")),
            "ceiling_camera": _yn(attrs.get("Ceiling-mounted camera")),
            "web_conference_camera": _yn(attrs.get("Web Conference Camera")),
            "apple_tv": _yn(attrs.get("AppleTV")),
            "instructor_pc_equipped": _yn(attrs.get("Instructor PC Equipped")) or _yn(attrs.get("Instructor Station - PC Equipped")),
            "assistive_listening_device": _yn(attrs.get("Assistive Listening Device")),
            "whiteboards_count": int(attrs.get("White Board", 0) or 0),
        },
    )

    # 3) panoramas
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
